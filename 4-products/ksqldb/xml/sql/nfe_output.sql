--******************--
-- terminate queries
--******************--
TERMINATE CSAS_KSQLDB_STREAM_NFE_AVRO_0;

--******************--
-- drop streams
--******************--
DROP STREAM ksqldb_stream_nfe_avro;

--******************--
-- remove topic
--******************--
k exec edh-kafka-0 -c kafka -i -t -- bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic ksqldb-stream-nfe-avro

--******************--
-- create enriched object NFE
--******************--

CREATE STREAM ksqldb_stream_nfe_avro
WITH (KAFKA_TOPIC='ksqldb-stream-nfe-avro',VALUE_FORMAT='AVRO',REPLICAS=3)
AS
SELECT
ide.ROWKEY,
AS_VALUE(ide.ROWKEY) AS "business_key",
TIMESTAMPTOSTRING(ide.ROWTIME, 'yyyy-MM-dd HH:mm:ss',  'America/Sao_Paulo') AS "processing_time",
ide."cUF",
ide."cNF" ,
ide."nCFe",
ide."dEmi",
ide."hEmi",
ide."cDV",
ide."tpAmb",
ide."CNPJ",
ide."mod",
ide."numeroCaixa",
emit."CNPJ",
emit."xNome",
emit."xFant",
emit."enderEmit"->"xLgr" as "logradouro",
emit."enderEmit"->"xCpl" as "cpl",
emit."enderEmit"->"xBairro" as "bairro",
emit."enderEmit"->"xMun" as "municipio",
emit."enderEmit"->"CEP" as "CEP",
pgto."MP"->"cMP",
pgto."MP"->"vMP",
pgto."vTroco",
total."ICMSTot"->"vICMS",
total."ICMSTot"->"vProd",
total."ICMSTot"->"vDesc",
total."ICMSTot"->"vPIS",
total."ICMSTot"->"vCOFINS",
total."ICMSTot"->"vPISST",
total."ICMSTot"->"vCOFINSST",
total."ICMSTot"->"vOutro",
total."vCFe",
total."vCFeLei12741",
items."@nItem" as "nro_item",
items."prod"->"cProd",
items."prod"->"cEAN",
items."prod"->"xProd",
items."prod"->"NCM",
items."prod"->"CFOP",
items."prod"->"uCom",
items."prod"->"qCom",
items."prod"->"vUnCom",
items."prod"->"vProd",
items."prod"->"indRegra",
items."prod"->"vItem",
items."imposto"->"vItem12741",
items."imposto"->"ICMS"->"ICMS40"->"Orig" as "ICMS_Orig",
items."imposto"->"ICMS"->"ICMS40"->"CST" as "ICMS_CST",
items."imposto"->"PIS"->"PISNT"->"CST" as "PIS_CST",
items."imposto"->"COFINS"->"COFINSNT"->"CST" as "COFINS_CST",
dest."CPF"
FROM str_ide_json ide
INNER JOIN str_emit_json emit WITHIN 10 SECONDS
ON ide."ROWKEY" = emit.ROWKEY
INNER JOIN str_pgto_json pgto WITHIN 10 SECONDS
ON emit."ROWKEY" = pgto.ROWKEY
INNER JOIN str_total_json total WITHIN 10 SECONDS
ON pgto."ROWKEY" = total.ROWKEY
LEFT JOIN str_dest_json dest WITHIN 10 SECONDS
ON ide."ROWKEY" = dest.ROWKEY
INNER JOIN str_items_json items WITHIN 10 SECONDS
ON ide."ROWKEY" = items.ROWKEY
PARTITION BY ide.ROWKEY
EMIT CHANGES;

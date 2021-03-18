--******************--
-- drop streams
--******************--
DROP STREAM str_ide_json;
DROP STREAM str_emit_json;
DROP STREAM str_inf_adic_json;
DROP STREAM str_pgto_json;
DROP STREAM str_total_json;
DROP STREAM str_dest_json;
DROP STREAM str_items_json;

--******************--
-- create stream str_ide_json
--******************--

CREATE OR REPLACE STREAM str_ide_json
(
  ROWKEY VARCHAR KEY,
  "cUF" VARCHAR,
  "cNF" VARCHAR,
  "mod" VARCHAR,
  "nserieSAT" VARCHAR,
  "nCFe" VARCHAR,
  "dEmi" VARCHAR,
  "hEmi" VARCHAR,
  "cDV" VARCHAR,
  "tpAmb" VARCHAR,
  "CNPJ" VARCHAR,
  "signAC" VARCHAR,
  "assinaturaQRCODE" VARCHAR,
  "numeroCaixa" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-ide-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_emit_json
--******************--

CREATE OR REPLACE STREAM str_emit_json
(
  ROWKEY VARCHAR KEY,
  "CNPJ" VARCHAR,
  "xNome" VARCHAR,
  "xFant" VARCHAR,
  "enderEmit" STRUCT<"xLgr" VARCHAR,
                     "nro" VARCHAR,
                     "xCpl" VARCHAR,
                     "xBairro" VARCHAR,
                     "xMun" VARCHAR,
                     "CEP" VARCHAR>,
  "IE" VARCHAR,
  "cRegTrib" VARCHAR,
  "indRatISSQN" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-emit-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_inf_adic_json
--******************--

CREATE OR REPLACE STREAM str_inf_adic_json
(
  ROWKEY VARCHAR KEY,
  "infCpl" VARCHAR,
  "obsFisco" STRUCT<"@xCampo" VARCHAR,
                     "xTexto" VARCHAR>
)
WITH (KAFKA_TOPIC='src-app-inf-adic-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_pgto_json
--******************--

CREATE OR REPLACE STREAM str_pgto_json
(
  ROWKEY VARCHAR KEY,
  "MP" STRUCT<"cMP" VARCHAR,
              "vMP" VARCHAR>,
  "vTroco" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-pgto-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_total_json
--******************--

CREATE OR REPLACE STREAM str_total_json
(
  ROWKEY VARCHAR KEY,
  "ICMSTot" STRUCT<"vICMS" VARCHAR,
                   "vProd" VARCHAR,
                   "vDesc" VARCHAR,
                   "vPIS" VARCHAR,
                   "vCOFINS" VARCHAR,
                   "vPISST" VARCHAR,
                   "vCOFINSST" VARCHAR,
                   "vOutro" VARCHAR>,
"vCFe" VARCHAR,
"vCFeLei12741" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-total-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_dest_json
--******************--

CREATE OR REPLACE STREAM str_dest_json
(
  ROWKEY VARCHAR KEY,
  "CPF" VARCHAR
)
WITH (KAFKA_TOPIC='src-app-dest-json', VALUE_FORMAT='JSON');


--******************--
-- create stream str_items_json
--******************--

CREATE OR REPLACE STREAM str_items_json
(
 ROWKEY VARCHAR KEY,
"@nItem" INT,
"prod" STRUCT<"cProd" VARCHAR,
              "cEAN" VARCHAR,
              "xProd" VARCHAR,
              "NCM" VARCHAR,
              "CFOP" VARCHAR,
              "uCom" VARCHAR,
              "qCom" VARCHAR,
              "vUnCom" VARCHAR,
              "vProd" VARCHAR,
              "indRegra" VARCHAR,
              "vItem" VARCHAR,
              "obsFiscoDet" STRUCT<"@xCampoDet" VARCHAR,
                                   "xTextoDet" VARCHAR >>,
"imposto" STRUCT<"vItem12741" VARCHAR,
                 "ICMS" STRUCT<"ICMS40" STRUCT<"Orig" VARCHAR,
                                               "CST" VARCHAR>>,
                 "PIS" STRUCT<"PISNT" STRUCT<"CST" VARCHAR>>,
                 "COFINS" STRUCT<"COFINSNT" STRUCT<"CST" VARCHAR>>>
)
WITH (KAFKA_TOPIC='src-app-items-json', VALUE_FORMAT='JSON');

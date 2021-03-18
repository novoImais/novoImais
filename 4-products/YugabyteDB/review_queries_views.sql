-- create index on enriched_nfe
CREATE INDEX enriched_nfe_business_key_index ON public.enriched_nfe (business_key);

-- query enriched nfe
-- table name = enriched_nfe
SELECT COUNT(*)
FROM public.enriched_nfe;

SELECT *
FROM public.enriched_nfe
WHERE business_key = 'CFe35210101379480000106590006329230104905567117';

-- query data [vw]
-- vw_enriched_products_compare_market
DROP VIEW public.vw_enriched_products_compare_market;

CREATE VIEW public.vw_enriched_products_compare_market
AS
SELECT nfe.business_key,
       i.mercado_comparavel,
       prod.descplmer,
       prod.desgrpprd,
       prod.desctgprd,
       prod.dessubctgprd,
       prod.desmrcmer,
       prod.submarca,
       prod.tipo_produto,
       prod.derivacao_marca
FROM ((((enriched_nfe nfe
JOIN imais.produto prod ON ((nfe."cEAN" = prod.codbrrundvndcsm)))
JOIN imais.cliente cli ON ((nfe."EMIT_CNPJ" = cli.numcgccpfclifrm)))
JOIN imais.mercado_comparavel i ON ((cli.codmnccli = i.codmnccli)))
JOIN imais.mercado imi ON ((cli.codmnccli = imi.codmnccli)));

-- time taken - 36 seconds [1]
-- count - 1.329.952
SELECT COUNT(*)
FROM public.vw_enriched_products_compare_market;

-- time taken - [3] seconds
SELECT *
FROM public.vw_enriched_products_compare_market
LIMIT 100;

SELECT *
FROM public.vw_enriched_products_compare_market
WHERE business_key = 'CFe35210101379480000106590006329230104905567117';

-- analyze query
EXPLAIN ANALYZE SELECT COUNT(*) FROM public.vw_enriched_products_compare_market;
EXPLAIN ANALYZE SELECT * FROM public.vw_enriched_products_compare_market;

-- verify indexes
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname IN ('public', 'imais')
ORDER BY tablename, indexname;

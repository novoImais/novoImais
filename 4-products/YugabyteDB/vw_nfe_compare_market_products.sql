--******************--
-- count nfe enriched table
-- yugabytedb
--******************--

CREATE VIEW vw_enriched_products_compare_market
AS
SELECT
 i.mercado_comparavel
,prod.DESCPLMER
,prod.DESGRPPRD
,prod.DESCTGPRD
,prod.DESSUBCTGPRD
,prod.DESMRCMER
,prod.SUBMARCA
,prod.TIPO_PRODUTO
,prod.DERIVACAO_MARCA
FROM  enriched_nfe nfe
INNER JOIN imais.produto prod ON nfe."cEAN"  = prod.codbrrundvndcsm
INNER JOIN imais.cliente cli ON nfe."EMIT_CNPJ" = cli.numcgccpfclifrm
INNER JOIN imais.mercado_comparavel i ON cli.codmnccli = i.codmnccli
INNER JOIN imais.mercado imi ON cli.codmnccli = imi.codmnccli;

SELECT COUNT(*)
FROM public.vw_enriched_products_compare_market;

SELECT *
FROM public.vw_enriched_products_compare_market
LIMIT 10;

--******************--
-- count nfe enriched table
-- postgres
--******************--

CREATE VIEW vw_enriched_products_compare_market
AS
SELECT
 i.mercado_comparavel
,prod.DESCPLMER
,prod.DESGRPPRD
,prod.DESCTGPRD
,prod.DESSUBCTGPRD
,prod.DESMRCMER
,prod.SUBMARCA
,prod.TIPO_PRODUTO
,prod.DERIVACAO_MARCA
FROM  enriched_nfe nfe
INNER JOIN public.produto prod ON nfe."cEAN"  = prod.codbrrundvndcsm
INNER JOIN public.cliente cli ON nfe."EMIT_CNPJ" = cli.numcgccpfclifrm
INNER JOIN public.mercado_comparavel i ON cli.codmnccli = i.codmnccli
INNER JOIN public.mercado imi ON cli.codmnccli = imi.codmnccli;

SELECT COUNT(*)
FROM public.vw_enriched_products_compare_market;

SELECT *
FROM public.vw_enriched_products_compare_market
LIMIT 10;

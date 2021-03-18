--******************--
-- count raw nfe enriched table
--******************--

SELECT COUNT(*)
FROM enriched_nfe;

--******************--
-- yugabytedb
-- count join nfe_compareMarket_products
--******************--

SELECT COUNT(*)
FROM  enriched_nfe nfe
INNER JOIN imais.produto prod ON nfe."cEAN"  = prod.codbrrundvndcsm
INNER JOIN imais.cliente cli ON nfe."EMIT_CNPJ" = cli.numcgccpfclifrm
INNER JOIN imais.mercado_comparavel i ON cli.codmnccli = i.codmnccli
INNER JOIN imais.mercado imi ON cli.codmnccli = imi.codmnccli;

--******************--
-- postgres
-- count join nfe_compareMarket_products
--******************--

SELECT COUNT(*)
FROM  enriched_nfe nfe
INNER JOIN public.produto prod ON nfe."cEAN"  = prod.codbrrundvndcsm
INNER JOIN public.cliente cli ON nfe."EMIT_CNPJ" = cli.numcgccpfclifrm
INNER JOIN public.mercado_comparavel i ON cli.codmnccli = i.codmnccli
INNER JOIN public.mercado imi ON cli.codmnccli = imi.codmnccli;

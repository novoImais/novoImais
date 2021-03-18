### accessing yugabytedb cli [ysqlsh]
```sh
# connecting into t-server and database
k exec yb-tserver-0 -c yb-tserver -i -t -- bash
./bin
ysqlsh -h 127.0.0.1 -p 5433 -U yugabyte
ysqlsh martins
```

### create indexes [idx]
```sh
# building indexes to optimize overall queries

# table = public.enriched_nfe
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_include_enriched_nfe_cean;'
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_include_enriched_nfe_emit_cnpj;'

ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_include_enriched_nfe_cean ON public.enriched_nfe ("cEAN") INCLUDE ("business_key");'
ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_include_enriched_nfe_emit_cnpj ON public.enriched_nfe ("EMIT_CNPJ") INCLUDE ("business_key");'

# table = imais.produto
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_include_produto;'
ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_include_produto ON imais.produto ("codbrrundvndcsm") INCLUDE("descplmer","desgrpprd","desctgprd","dessubctgprd","desmrcmer","submarca","tipo_produto","derivacao_marca");'

# table = imais.cliente
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_cliente;'
ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_cliente ON imais.cliente ("numcgccpfclifrm","codmnccli");'

# table = imais.mercado_comparavel
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_include_mercado_comparavel;'
ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_include_mercado_comparavel ON imais.mercado_comparavel ("codmnccli") INCLUDE ("mercado_comparavel");'

# table = imais.mercado
ysqlsh -d martins -c '\x' -c 'DROP INDEX ci_index_mercado;'
ysqlsh -d martins -c '\x' -c 'CREATE INDEX ci_index_mercado ON imais.mercado ("codmnccli");'
```

### verify logs
```sh
# verify logs
k logs yb-tserver-0 -c yb-tserver -f
```

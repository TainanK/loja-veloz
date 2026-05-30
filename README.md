# Loja Veloz - Projeto de microsservicos com Docker e Kubernetes

Projeto desenvolvido para a disciplina de Cloud DevOps. A ideia foi pegar uma aplicacao de e-commerce simples e estruturar ela toda em microsservicos, com ambiente local usando Docker Compose e deploy em Kubernetes.

## Como a aplicacao esta organizada

A aplicacao tem 4 servicos principais que se comunicam entre si:

```
usuario -> api-gateway (porta 8000)
               |
    ┌──────────┼──────────┐
    |          |          |
 pedidos   pagamentos  estoque
 (8001)     (8002)     (8003)
    |
 postgres
 (5432)
```

O api-gateway recebe todas as requisicoes e repassa para o servico correto. Os servicos de pagamentos e estoque ficam so acessiveis internamente.

## Como rodar localmente

Precisa ter o Docker instalado. Com ele instalado, so rodar:

```bash
# copia o arquivo de variaveis
cp .env.example .env

# sobe tudo
docker compose up --build
```

Depois de subir, da pra acessar:
- api-gateway: http://localhost:8000
- documentacao: http://localhost:8000/docs
- pedidos direto: http://localhost:8001
- pagamentos direto: http://localhost:8002
- estoque direto: http://localhost:8003

## Testando os endpoints

```bash
# ver se esta rodando
curl http://localhost:8000/health

# criar um pedido
curl -X POST http://localhost:8001/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente": "Joao", "produto_id": 1, "quantidade": 2}'

# consultar estoque
curl http://localhost:8003/estoque/1

# processar pagamento
curl -X POST http://localhost:8002/pagamentos \
  -H "Content-Type: application/json" \
  -d '{"pedido_id": 1, "valor": 99.90, "metodo": "pix"}'
```

## Rodando no Kubernetes

```bash
kubectl create namespace lojaveloz
kubectl apply -f k8s/configmaps/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
```

## Pipeline CI/CD

O arquivo `.github/workflows/ci-cd.yml` configura o pipeline automatico. Quando sobe codigo na branch main ele roda lint, faz o build das imagens e faz o deploy no cluster.

Para funcionar precisa configurar o secret `KUBE_CONFIG` no repositorio do GitHub.

## Infraestrutura como codigo

A pasta `terraform/` tem o esqueleto para criar o namespace e as quotas de recurso no Kubernetes usando Terraform.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Estrutura de pastas

```
loja-veloz/
├── services/
│   ├── api-gateway/
│   ├── pedidos/
│   ├── pagamentos/
│   └── estoque/
├── k8s/
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   └── secrets/
├── .github/workflows/
├── terraform/
└── docker-compose.yml
```

## Video

link:

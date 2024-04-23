# RAG_bot
Le cygne majestueux sillionant le lac des internets


az acr task create --registry $ACR_NAME --name taskhelloworld --image helloworld:{{.Run.ID}} --context https://github.com/$GIT_USER/acr-build-helloworld-node.git#master --file Dockerfile --git-access-token $GIT_PAT

az acr task create --registry $ACR_NAME --name taskragbot --image ragbot:{{.Run.ID}} --context https://github.com/$GIT_USER/RAG_bot.git#main --file Dockerfile --git-access-token $GIT_PAT
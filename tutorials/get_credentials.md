# Como Gerar as Credenciais do Gmail

Esse arquivo Markdown serve para que se torne de "conhecimento público" o método de conexão para com o provedor de e-mails, visto que há a chance de mudança de protocolo por parte do google e essa senha tenha que ser gerada novamente.

Lembre-se: é muito difícil que esse processo tenha que ser utilizado. Eu só ativaria no caso de um colaborador mau intencionado que tenha a senha ou até mesmo de uma troca de operação. É mais como um mecanismo de segurança que passa pela autenticação da Dinara. Dito isso, lá vamos nós:

1. Acesse o navegador com o Gmail do copeboletos@gmail.com

2. Acesse [esse link](https://myaccount.google.com/apppasswords)

3. Será necessário confirmação pelo celular da Dinara. Pois colocamos autenticação de dois fatores no processo de geração de senhas.

4. Para gerar a nova senha (se necessário) basta "criar um novo app", com o tipo de app sendo "E-mail" e o dispositivo correspondente.

5. Ao gerar o novo app, serão dadas as credenciais necessárias para substituir no arquivo "creds.json", que é consumido pelo código principal. Lembre-se que caso estejando alterando por motivos de segurança, exclua os apps antigos.


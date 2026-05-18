# 🖋️ Sistema de Plataforma de Tatuagens

Uma rede social especializada para conectar clientes, artistas tatuadores e estúdios de tatuagem, facilitando o agendamento e a divulgação de portfólios.

---

## 📑 Sumário
- [Descrição Geral](#-descrição-geral)
- [Tipos de Usuários](#-tipos-de-usuários)
- [Regras de Negócio (RN)](#-regras-de-negócio-rn)
- [Funcionalidades e Interações](#-funcionalidades-e-interações)
- [Segurança e Moderação](#-segurança-e-moderação)
- [Tecnologias](#-tecnologias)

---

## 📖 Descrição Geral
A plataforma funciona como um ecossistema completo para o mundo da tatuagem, permitindo:
* **Divulgação:** Portfólios dinâmicos para artistas.
* **Interação:** Curtidas, comentários e salvamentos de posts.
* **Gestão:** Agendamento de serviços e comunicação direta.
* **Confiança:** Sistema de avaliações de artistas e estúdios.

---

## 👥 Tipos de Usuários

| Perfil | Descrição |
| :--- | :--- |
| **Cliente** | Usuário que busca artistas, interage com posts, realiza agendamentos e avalia serviços. |
| **Artista** | Profissional que publica trabalhos, oferece serviços e pode gerenciar ou participar de um estúdio. |
| **Admin do Estúdio** | Um Artista com permissões administrativas para gerenciar membros e informações do estúdio. |

---

## 🛠️ Regras de Negócio (RN)

### 01. Cadastro e Perfil
* **RN01 (Cadastro):** Requer nome, email único, senha e telefone. O usuário deve escolher entre perfil Cliente ou Artista.
* **RN02 (Perfil):** Liberdade para atualização de bio, fotos e contatos.

### 02. Gestão de Estúdios
* **RN03 (Criação):** Exclusiva para artistas. O criador torna-se o administrador.
* **RN05 (Vínculo):** Um artista pode estar em apenas **um** estúdio por vez.
* **RN06 (Ingresso):** Depende de solicitação do artista e aprovação do administrador do estúdio.

### 03. Conteúdo e Portfólio
* **RN07/08 (Posts):** Suporte a imagens, vídeos, descrições e orçamentos estimados. Estúdios também podem postar em nome da marca.
* **RN09 (Portfólio):** Vitrine automática baseada nas publicações do artista.

### 04. Agendamentos
* **RN16 (Solicitação):** O cliente define data, hora e serviço.
* **RN17 (Fluxo):** O artista controla o status: `Pendente` → `Confirmado` / `Cancelado` → `Concluído`.

### 05. Ciclo de Vida dos Dados
* **RN20 (Exclusão de Conta):** Remove todos os dados do usuário e suas postagens permanentemente.
* **RN21 (Exclusão de Post):** Remove a mídia e todas as interações (curtidas/comentários) vinculadas.

---

## 💬 Funcionalidades e Interações
* **Social:** Curtida única por postagem e sistema de comentários rastreáveis.
* **Mensageria:** Chat direto entre as partes interessadas.
* **Avaliações:** Notas de 1 a 5 para profissionais e estabelecimentos.
* **Favoritos:** Lista de salvamentos para referência futura do cliente.

---

## 🔒 Segurança e Moderação
* **RN18:** Monitoramento e remoção de conteúdos ofensivos ou inadequados.
* **RN19:** Garantia de unicidade de conta via e-mail.

---

## 🚀 Próximos Passos (Backlog)
- [ ] Sistema de Seguidores e Feed Personalizado.
- [ ] Integração com Mapas (Localização de estúdios próximos).
- [ ] Sistema de Notificações Push/In-app.
- [ ] Agenda visual para o Artista.
- [ ] Canal de Denúncias.

---

## 💻 Tecnologias
* **Banco de Dados:** PostgreSQL

=======
* **Back-End:** Flask Python


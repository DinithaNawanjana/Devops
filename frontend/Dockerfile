# Dev-mode container (hot reload). For production, swap to `next build` +
# `next start` in a multi-stage build.
FROM node:22-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]

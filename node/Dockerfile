FROM node:14-alpine

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/service_account.json

WORKDIR /app

COPY ["package-lock.json", "package.json", "./"]

RUN npm install --production

EXPOSE 3000

CMD ["npm", "start"]


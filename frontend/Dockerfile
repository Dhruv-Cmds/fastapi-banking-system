FROM node:22.22.2

WORKDIR /app


COPY package*.json ./

RUN npm install


COPY . .


EXPOSE 5173


CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
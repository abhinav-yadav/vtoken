FROM node:9
RUN mkdir /app
WORKDIR /app
COPY package.json /app
COPY bitcorelib.js /app
RUN npm install
COPY . /app
RUN rm node_modules/bitcore-lib/index.js
RUN mv bitcorelib.js node_modules/bitcore-lib/index.js
EXPOSE 3000
CMD ["npm", "start"]
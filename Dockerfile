FROM node:22-alpine AS build
WORKDIR /build
COPY package.json ./
RUN npm install
COPY src ./src
COPY *.html ./
RUN npm run build

FROM nginx:alpine

# Copy website files to nginx
COPY *.html /usr/share/nginx/html/
COPY *.png /usr/share/nginx/html/
COPY images /usr/share/nginx/html/images
COPY nav.html /usr/share/nginx/html/
COPY --from=build /build/styles.css /usr/share/nginx/html/styles.css

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

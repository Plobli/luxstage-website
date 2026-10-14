FROM node:22-alpine AS build
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY src ./src
COPY tools ./tools
COPY *.html *.js *.png *.txt *.xml ./
COPY fonts ./fonts
COPY images ./images
# Tailwind-CSS bauen und Navigation in die Seiten einsetzen (Ergebnis: dist/)
RUN npm run build

FROM nginx:alpine
COPY default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /build/dist /usr/share/nginx/html
ARG APP_VERSION=dev
RUN sed -i "s/__APP_VERSION__/${APP_VERSION}/g" /usr/share/nginx/html/*.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

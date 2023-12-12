# Use Node.js image
FROM node:latest

# Create working directory /app on the image
WORKDIR /app

# Copy package.json and package-lock.json to /app
COPY package*.json /app

# Install dependencies from package.json
RUN rm -rf node_modules
RUN npm install

# Copy all source code to /app
COPY . /app

# Build the application
RUN rm -rf dist
RUN npm install -g serve@10.1.1
RUN npm run build


# Declare the port the container listens to
EXPOSE 3000

# Run the serve service to serve the application
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
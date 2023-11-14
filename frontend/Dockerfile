# Use an official Node.js runtime as a parent image
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install pnpm
RUN npm install -g pnpm

# Copy only the package.json files (and not the entire project)
COPY vis-frontend/package.json ./
COPY vis-frontend/pnpm-lock.yaml* ./

# Install dependencies inside the container
RUN pnpm install

# Now copy the rest of your app's source code
COPY vis-frontend/ ./

# Make port 3000 available to the world outside this container
EXPOSE 5173

# Define the command to run your app
CMD ["pnpm", "run", "dev", "--", "--host"]

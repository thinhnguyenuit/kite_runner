const path = require("path");

module.exports = {
  pages: {
    index: {
      entry: "frontend/src/main.js",
      template: "frontend/public/index.html",
    },
  },
  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "frontend/src"),
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin("copy").use(require("copy-webpack-plugin"), [
      [
        {
          from: path.resolve(__dirname, "frontend/public"),
          to: path.resolve(__dirname, "dist"),
          toType: "dir",
          ignore: [".DS_Store"],
        },
      ],
    ]);
  },
};

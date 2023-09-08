const path = require("path");

module.exports = {
  mode: "development",
  entry: "./WebInterface/js/main.jsx",
  output: {
    path: path.join(__dirname, "/WebInterface/static/js/"),
    filename: "bundle.js",
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        // Test for js or jsx files
        test: /\.jsx?$/,
        // Exclude external modules from loader tests
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/preset-env", "@babel/preset-react"],
          plugins: ["@babel/transform-runtime"],
        },
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
};

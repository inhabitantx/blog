

const config = {
  entry:["babel-polyfill","./static/js/react-components/index.js"],
  output: {
    path: __dirname + '/static/js',
    filename: "bundle.js"
  },
  module: {
      rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
          use: [
            {
              loader: 'babel-loader',

           }]
      }]
  }

};
module.exports = config;

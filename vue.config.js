module.exports = {
  transpileDependencies: ['vuetify'],
  configureWebpack: {
    devtool: 'source-map',
  },
  chainWebpack: (config) => {
    config.plugin('html').tap((args) => {
      args[0].title = '家禽價格分析';
      return args;
    });
  },
  devServer: {
    overlay: {
      warnings: true,
      errors: true
    }
  },
  pluginOptions: {
    electronBuilder: {
      nodeIntegration: true,
      builderOptions: {
        appId: 'xyz.yurina.poultrypriceanalysis',
        productName: '家禽價格分析',
      },
    },
  },
};

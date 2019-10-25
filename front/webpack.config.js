const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: {
        site: './src/index.js',
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'style.bundle.css',
            chunkFilename: '[id].css',
            ignoreOrder: false,
        }),
        new HtmlWebpackPlugin({
            template: path.resolve('./index.html')
        }),
        new webpack.EnvironmentPlugin(['NODE_ENV', 'USE_LOCALHOST', 'LOCALHOST_ADDRESS', 'REMOTE_ADDRESS'])
    ],
    module: {
        rules: [{
            test: /\.(jpg|jpeg|png|gif)$/i,
            use: {
                loader: 'file-loader',
                options: {
                    name: 'static/img/[name].[ext]'
                }
            }
        },
            {
                test: /\.m?js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.s(a|c)ss$/,
                loader: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            modules: true,
                            localIdentName: '[hash:base64:5]',
                            sourceMap: false
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: false
                        }
                    }
                ]
            },
            {
                test: /\.s(a|c)ss$/,
                exclude: /.(s(a|c)ss)$/,
                loader: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: false
                        }
                    }
                ]
            }
        ],
    },
    watch: (process.env.NODE_ENV === 'development'),
    devtool: (process.env.NODE_ENV === 'development') ? 'cheap-inline-module-source-map' : false,
    output: {
        filename: 'bundle.min.js',
        path: path.resolve('./build/'), //./build/
        publicPath: "/"
    },
    resolve: {
        extensions: ['.js', '.jsx', '.scss'],
        alias: {
            'react': 'preact-compat',
            'react-dom': 'preact-compat'
        }
    },
    devServer: {
        historyApiFallback: true,
        contentBase: path.join(__dirname, './build'),
        compress: true,
        // host: '0.0.0.0',
        watchOptions: {aggregateTimeout: 300, poll: 1000},
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
            "Access-Control-Allow-Headers": "X-Requested-With, content-type, Authorization"
        }
    },
};
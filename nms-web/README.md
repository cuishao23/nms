# nms-web

## 1.Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

For a detailed explanation on how things work, check out the [guide](http://vuejs-templates.github.io/webpack/) and [docs for vue-loader](http://vuejs.github.io/vue-loader).


## 2.src目录结构约束

```
./src
|-- assets
|-- axios
|-- common         --> 公共模块 组件
|-- components     --> 页面组件
|-- mock    
|-- pages          --> 页面框架
|-- router
|-- store
`-- ws
```
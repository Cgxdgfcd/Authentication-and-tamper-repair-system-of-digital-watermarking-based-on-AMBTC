webpackJsonp([2],{"+qVd":function(t,e){},"996y":function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n("Dd8w"),o=n.n(i),r=n("7+uW"),s=n("NYxO");r.default.use(s.a);var a=new s.a.Store({state:{isPractice:!1,flag:!0,userInfo:null,menu:[{index:"1",title:"图片管理",no:"嵌入水印",icon:"el-icon-s-data",content:[{item1:"嵌入水印",path:"/EmbedWatermark",icon:"el-icon-circle-plus-outline"},{item2:"区域检测",path:"/AreaDetection",icon:"el-icon-zoom-in"},{item3:"恢复图片",path:"/RestorePicture",icon:"el-icon-key"}]}]},mutations:{practice:function(t,e){t.isPractice=e},toggle:function(t){t.flag=!t.flag},changeUserInfo:function(t,e){t.userInfo=e}},getters:{},actions:{getUserInfo:function(t,e){t.commit("changeUserInfo",e)},getPractice:function(t,e){t.commit("practice",e)}}}),c={data:function(){return{login_flag:!1,user:{userName:null,userId:null}}},created:function(){this.getUserInfo()},computed:Object(s.c)(["flag","menu"]),methods:o()({showSetting:function(){this.login_flag=!this.login_flag}},Object(s.b)(["toggle"]),{getUserInfo:function(){this.user.userName="张三",this.user.userId=123},index:function(){},exit:function(){var t=this.$cookies.get("role");this.$router.push({path:"/"}),this.$cookies.remove("cname"),this.$cookies.remove("cid"),this.$cookies.remove("role"),0==t&&this.menu.pop()}}),store:a},u={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"top_head"}},[n("header",{attrs:{id:"topbar"}},[n("el-row",[n("el-col",{staticClass:"topbar-left",attrs:{span:6}},[n("i",{staticClass:"el-icon-s-promotion"}),t._v(" "),n("span",{staticClass:"title",on:{click:function(e){t.index()}}},[t._v("数字水印的嵌入与篡改修复系统")])]),t._v(" "),n("el-col",{staticClass:"topbar-right",attrs:{span:18}},[n("i",{class:[t.flag?"el-icon-s-unfold":"el-icon-s-fold"],on:{click:function(e){t.toggle()}}})])],1)],1)])},staticRenderFns:[]};var l=n("VU/8")(c,u,!1,function(t){n("rrSr")},"data-v-86d875f2",null).exports,f={name:"mainLeft",data:function(){return{elmenuitemischoose:[!1,!1,!1,!1],currentelmenuitem:null}},computed:Object(s.c)(["flag","menu"]),created:function(){this.addData()},methods:{handleOpen:function(t,e){},handleClose:function(t,e){},handleTitle:function(t){null!=this.currentelmenuitem&&(this.elmenuitemischoose[this.currentelmenuitem]=!1),this.elmenuitemischoose[t]=!0,this.currentelmenuitem=t},addData:function(){}},store:a},h={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"left"}},[n("el-menu",{staticClass:"el-menu-vertical-demo",attrs:{"active-text-color":"darkturquoise","text-color":"#ffffff","default-active":this.$route.path,collapse:t.flag,"unique-opened":"true","background-color":"#124280","menu-trigger":"click",router:""},on:{open:t.handleOpen,close:t.handleClose}},[n("el-menu-item",{staticClass:"el-menu-item",attrs:{index:"/"},on:{click:function(e){t.handleTitle(0)}}},[n("div",{class:[t.elmenuitemischoose[0]?"selected-left-width":"left-width"]},[n("i",{staticClass:"iconfont",class:"el-icon-s-home"}),t._v(" "),n("span",{staticClass:"title",attrs:{slot:"title"},slot:"title"},[t._v("首页")])])]),t._v(" "),n("el-menu-item",{staticClass:"el-menu-item",attrs:{index:"/EmbedWatermark"},on:{click:function(e){t.handleTitle(1)}}},[n("div",{class:[t.elmenuitemischoose[1]?"selected-left-width":"left-width"]},[n("i",{staticClass:"iconfont",class:"el-icon-circle-plus-outline"}),t._v(" "),n("span",{staticClass:"title",attrs:{slot:"title"},slot:"title"},[t._v("嵌入水印")])])]),t._v(" "),n("el-menu-item",{staticClass:"el-menu-item",attrs:{index:"/AreaDetection"},on:{click:function(e){t.handleTitle(2)}}},[n("div",{class:[t.elmenuitemischoose[2]?"selected-left-width":"left-width"]},[n("i",{staticClass:"iconfont",class:"el-icon-zoom-in"}),t._v(" "),n("span",{staticClass:"title",attrs:{slot:"title"},slot:"title"},[t._v("图像认证")])])]),t._v(" "),n("el-menu-item",{staticClass:"el-menu-item",attrs:{index:"/RestorePicture"},on:{click:function(e){t.handleTitle(3)}}},[n("div",{class:[t.elmenuitemischoose[3]?"selected-left-width":"left-width"]},[n("i",{staticClass:"iconfont",class:"el-icon-key"}),t._v(" "),n("span",{staticClass:"title",attrs:{slot:"title"},slot:"title"},[t._v("篡改恢复")])])])],1)],1)},staticRenderFns:[]};var d={components:{header1:l,mainLeft:n("VU/8")(f,h,!1,function(t){n("+qVd")},"data-v-2d2bb886",null).exports,navigator:navigator},data:function(){return{username:""}},methods:{}},p={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"index"}},[e("header1",{staticClass:"topbar"}),this._v(" "),e("section",{staticClass:"container"},[e("div",{staticClass:"left_side"},[e("mainLeft")],1),this._v(" "),e("div",{staticClass:"main_wrapper"},[e("router-view")],1)])],1)},staticRenderFns:[]};var m=n("VU/8")(d,p,!1,function(t){n("qspk")},"data-v-670ba1b9",null);e.default=m.exports},NYxO:function(t,e,n){"use strict";(function(t){n.d(e,"b",function(){return w}),n.d(e,"c",function(){return b});var i=("undefined"!=typeof window?window:void 0!==t?t:{}).__VUE_DEVTOOLS_GLOBAL_HOOK__;function o(t,e){if(void 0===e&&(e=[]),null===t||"object"!=typeof t)return t;var n,i=(n=function(e){return e.original===t},e.filter(n)[0]);if(i)return i.copy;var r=Array.isArray(t)?[]:{};return e.push({original:t,copy:r}),Object.keys(t).forEach(function(n){r[n]=o(t[n],e)}),r}function r(t,e){Object.keys(t).forEach(function(n){return e(t[n],n)})}function s(t){return null!==t&&"object"==typeof t}var a=function(t,e){this.runtime=e,this._children=Object.create(null),this._rawModule=t;var n=t.state;this.state=("function"==typeof n?n():n)||{}},c={namespaced:{configurable:!0}};c.namespaced.get=function(){return!!this._rawModule.namespaced},a.prototype.addChild=function(t,e){this._children[t]=e},a.prototype.removeChild=function(t){delete this._children[t]},a.prototype.getChild=function(t){return this._children[t]},a.prototype.hasChild=function(t){return t in this._children},a.prototype.update=function(t){this._rawModule.namespaced=t.namespaced,t.actions&&(this._rawModule.actions=t.actions),t.mutations&&(this._rawModule.mutations=t.mutations),t.getters&&(this._rawModule.getters=t.getters)},a.prototype.forEachChild=function(t){r(this._children,t)},a.prototype.forEachGetter=function(t){this._rawModule.getters&&r(this._rawModule.getters,t)},a.prototype.forEachAction=function(t){this._rawModule.actions&&r(this._rawModule.actions,t)},a.prototype.forEachMutation=function(t){this._rawModule.mutations&&r(this._rawModule.mutations,t)},Object.defineProperties(a.prototype,c);var u=function(t){this.register([],t,!1)};u.prototype.get=function(t){return t.reduce(function(t,e){return t.getChild(e)},this.root)},u.prototype.getNamespace=function(t){var e=this.root;return t.reduce(function(t,n){return t+((e=e.getChild(n)).namespaced?n+"/":"")},"")},u.prototype.update=function(t){!function t(e,n,i){0;n.update(i);if(i.modules)for(var o in i.modules){if(!n.getChild(o))return void 0;t(e.concat(o),n.getChild(o),i.modules[o])}}([],this.root,t)},u.prototype.register=function(t,e,n){var i=this;void 0===n&&(n=!0);var o=new a(e,n);0===t.length?this.root=o:this.get(t.slice(0,-1)).addChild(t[t.length-1],o);e.modules&&r(e.modules,function(e,o){i.register(t.concat(o),e,n)})},u.prototype.unregister=function(t){var e=this.get(t.slice(0,-1)),n=t[t.length-1],i=e.getChild(n);i&&i.runtime&&e.removeChild(n)},u.prototype.isRegistered=function(t){var e=this.get(t.slice(0,-1)),n=t[t.length-1];return!!e&&e.hasChild(n)};var l;var f=function(t){var e=this;void 0===t&&(t={}),!l&&"undefined"!=typeof window&&window.Vue&&y(window.Vue);var n=t.plugins;void 0===n&&(n=[]);var o=t.strict;void 0===o&&(o=!1),this._committing=!1,this._actions=Object.create(null),this._actionSubscribers=[],this._mutations=Object.create(null),this._wrappedGetters=Object.create(null),this._modules=new u(t),this._modulesNamespaceMap=Object.create(null),this._subscribers=[],this._watcherVM=new l,this._makeLocalGettersCache=Object.create(null);var r=this,s=this.dispatch,a=this.commit;this.dispatch=function(t,e){return s.call(r,t,e)},this.commit=function(t,e,n){return a.call(r,t,e,n)},this.strict=o;var c=this._modules.root.state;v(this,c,[],this._modules.root),m(this,c),n.forEach(function(t){return t(e)}),(void 0!==t.devtools?t.devtools:l.config.devtools)&&function(t){i&&(t._devtoolHook=i,i.emit("vuex:init",t),i.on("vuex:travel-to-state",function(e){t.replaceState(e)}),t.subscribe(function(t,e){i.emit("vuex:mutation",t,e)},{prepend:!0}),t.subscribeAction(function(t,e){i.emit("vuex:action",t,e)},{prepend:!0}))}(this)},h={state:{configurable:!0}};function d(t,e,n){return e.indexOf(t)<0&&(n&&n.prepend?e.unshift(t):e.push(t)),function(){var n=e.indexOf(t);n>-1&&e.splice(n,1)}}function p(t,e){t._actions=Object.create(null),t._mutations=Object.create(null),t._wrappedGetters=Object.create(null),t._modulesNamespaceMap=Object.create(null);var n=t.state;v(t,n,[],t._modules.root,!0),m(t,n,e)}function m(t,e,n){var i=t._vm;t.getters={},t._makeLocalGettersCache=Object.create(null);var o={};r(t._wrappedGetters,function(e,n){o[n]=function(t,e){return function(){return t(e)}}(e,t),Object.defineProperty(t.getters,n,{get:function(){return t._vm[n]},enumerable:!0})});var s=l.config.silent;l.config.silent=!0,t._vm=new l({data:{$$state:e},computed:o}),l.config.silent=s,t.strict&&function(t){t._vm.$watch(function(){return this._data.$$state},function(){0},{deep:!0,sync:!0})}(t),i&&(n&&t._withCommit(function(){i._data.$$state=null}),l.nextTick(function(){return i.$destroy()}))}function v(t,e,n,i,o){var r=!n.length,s=t._modules.getNamespace(n);if(i.namespaced&&(t._modulesNamespaceMap[s],t._modulesNamespaceMap[s]=i),!r&&!o){var a=g(e,n.slice(0,-1)),c=n[n.length-1];t._withCommit(function(){l.set(a,c,i.state)})}var u=i.context=function(t,e,n){var i=""===e,o={dispatch:i?t.dispatch:function(n,i,o){var r=_(n,i,o),s=r.payload,a=r.options,c=r.type;return a&&a.root||(c=e+c),t.dispatch(c,s)},commit:i?t.commit:function(n,i,o){var r=_(n,i,o),s=r.payload,a=r.options,c=r.type;a&&a.root||(c=e+c),t.commit(c,s,a)}};return Object.defineProperties(o,{getters:{get:i?function(){return t.getters}:function(){return function(t,e){if(!t._makeLocalGettersCache[e]){var n={},i=e.length;Object.keys(t.getters).forEach(function(o){if(o.slice(0,i)===e){var r=o.slice(i);Object.defineProperty(n,r,{get:function(){return t.getters[o]},enumerable:!0})}}),t._makeLocalGettersCache[e]=n}return t._makeLocalGettersCache[e]}(t,e)}},state:{get:function(){return g(t.state,n)}}}),o}(t,s,n);i.forEachMutation(function(e,n){!function(t,e,n,i){(t._mutations[e]||(t._mutations[e]=[])).push(function(e){n.call(t,i.state,e)})}(t,s+n,e,u)}),i.forEachAction(function(e,n){var i=e.root?n:s+n,o=e.handler||e;!function(t,e,n,i){(t._actions[e]||(t._actions[e]=[])).push(function(e){var o,r=n.call(t,{dispatch:i.dispatch,commit:i.commit,getters:i.getters,state:i.state,rootGetters:t.getters,rootState:t.state},e);return(o=r)&&"function"==typeof o.then||(r=Promise.resolve(r)),t._devtoolHook?r.catch(function(e){throw t._devtoolHook.emit("vuex:error",e),e}):r})}(t,i,o,u)}),i.forEachGetter(function(e,n){!function(t,e,n,i){if(t._wrappedGetters[e])return void 0;t._wrappedGetters[e]=function(t){return n(i.state,i.getters,t.state,t.getters)}}(t,s+n,e,u)}),i.forEachChild(function(i,r){v(t,e,n.concat(r),i,o)})}function g(t,e){return e.reduce(function(t,e){return t[e]},t)}function _(t,e,n){return s(t)&&t.type&&(n=e,e=t,t=t.type),{type:t,payload:e,options:n}}function y(t){l&&t===l||
/*!
 * vuex v3.6.2
 * (c) 2021 Evan You
 * @license MIT
 */
function(t){if(Number(t.version.split(".")[0])>=2)t.mixin({beforeCreate:n});else{var e=t.prototype._init;t.prototype._init=function(t){void 0===t&&(t={}),t.init=t.init?[n].concat(t.init):n,e.call(this,t)}}function n(){var t=this.$options;t.store?this.$store="function"==typeof t.store?t.store():t.store:t.parent&&t.parent.$store&&(this.$store=t.parent.$store)}}(l=t)}h.state.get=function(){return this._vm._data.$$state},h.state.set=function(t){0},f.prototype.commit=function(t,e,n){var i=this,o=_(t,e,n),r=o.type,s=o.payload,a=(o.options,{type:r,payload:s}),c=this._mutations[r];c&&(this._withCommit(function(){c.forEach(function(t){t(s)})}),this._subscribers.slice().forEach(function(t){return t(a,i.state)}))},f.prototype.dispatch=function(t,e){var n=this,i=_(t,e),o=i.type,r=i.payload,s={type:o,payload:r},a=this._actions[o];if(a){try{this._actionSubscribers.slice().filter(function(t){return t.before}).forEach(function(t){return t.before(s,n.state)})}catch(t){0}var c=a.length>1?Promise.all(a.map(function(t){return t(r)})):a[0](r);return new Promise(function(t,e){c.then(function(e){try{n._actionSubscribers.filter(function(t){return t.after}).forEach(function(t){return t.after(s,n.state)})}catch(t){0}t(e)},function(t){try{n._actionSubscribers.filter(function(t){return t.error}).forEach(function(e){return e.error(s,n.state,t)})}catch(t){0}e(t)})})}},f.prototype.subscribe=function(t,e){return d(t,this._subscribers,e)},f.prototype.subscribeAction=function(t,e){return d("function"==typeof t?{before:t}:t,this._actionSubscribers,e)},f.prototype.watch=function(t,e,n){var i=this;return this._watcherVM.$watch(function(){return t(i.state,i.getters)},e,n)},f.prototype.replaceState=function(t){var e=this;this._withCommit(function(){e._vm._data.$$state=t})},f.prototype.registerModule=function(t,e,n){void 0===n&&(n={}),"string"==typeof t&&(t=[t]),this._modules.register(t,e),v(this,this.state,t,this._modules.get(t),n.preserveState),m(this,this.state)},f.prototype.unregisterModule=function(t){var e=this;"string"==typeof t&&(t=[t]),this._modules.unregister(t),this._withCommit(function(){var n=g(e.state,t.slice(0,-1));l.delete(n,t[t.length-1])}),p(this)},f.prototype.hasModule=function(t){return"string"==typeof t&&(t=[t]),this._modules.isRegistered(t)},f.prototype.hotUpdate=function(t){this._modules.update(t),p(this,!0)},f.prototype._withCommit=function(t){var e=this._committing;this._committing=!0,t(),this._committing=e},Object.defineProperties(f.prototype,h);var b=O(function(t,e){var n={};return $(e).forEach(function(e){var i=e.key,o=e.val;n[i]=function(){var e=this.$store.state,n=this.$store.getters;if(t){var i=x(this.$store,"mapState",t);if(!i)return;e=i.context.state,n=i.context.getters}return"function"==typeof o?o.call(this,e,n):e[o]},n[i].vuex=!0}),n}),w=O(function(t,e){var n={};return $(e).forEach(function(e){var i=e.key,o=e.val;n[i]=function(){for(var e=[],n=arguments.length;n--;)e[n]=arguments[n];var i=this.$store.commit;if(t){var r=x(this.$store,"mapMutations",t);if(!r)return;i=r.context.commit}return"function"==typeof o?o.apply(this,[i].concat(e)):i.apply(this.$store,[o].concat(e))}}),n}),C=O(function(t,e){var n={};return $(e).forEach(function(e){var i=e.key,o=e.val;o=t+o,n[i]=function(){if(!t||x(this.$store,"mapGetters",t))return this.$store.getters[o]},n[i].vuex=!0}),n}),k=O(function(t,e){var n={};return $(e).forEach(function(e){var i=e.key,o=e.val;n[i]=function(){for(var e=[],n=arguments.length;n--;)e[n]=arguments[n];var i=this.$store.dispatch;if(t){var r=x(this.$store,"mapActions",t);if(!r)return;i=r.context.dispatch}return"function"==typeof o?o.apply(this,[i].concat(e)):i.apply(this.$store,[o].concat(e))}}),n});function $(t){return function(t){return Array.isArray(t)||s(t)}(t)?Array.isArray(t)?t.map(function(t){return{key:t,val:t}}):Object.keys(t).map(function(e){return{key:e,val:t[e]}}):[]}function O(t){return function(e,n){return"string"!=typeof e?(n=e,e=""):"/"!==e.charAt(e.length-1)&&(e+="/"),t(e,n)}}function x(t,e,n){return t._modulesNamespaceMap[n]}function E(t,e,n){var i=n?t.groupCollapsed:t.group;try{i.call(t,e)}catch(n){t.log(e)}}function M(t){try{t.groupEnd()}catch(e){t.log("—— log end ——")}}function j(){var t=new Date;return" @ "+A(t.getHours(),2)+":"+A(t.getMinutes(),2)+":"+A(t.getSeconds(),2)+"."+A(t.getMilliseconds(),3)}function A(t,e){return n="0",i=e-t.toString().length,new Array(i+1).join(n)+t;var n,i}var S={Store:f,install:y,version:"3.6.2",mapState:b,mapMutations:w,mapGetters:C,mapActions:k,createNamespacedHelpers:function(t){return{mapState:b.bind(null,t),mapGetters:C.bind(null,t),mapMutations:w.bind(null,t),mapActions:k.bind(null,t)}},createLogger:function(t){void 0===t&&(t={});var e=t.collapsed;void 0===e&&(e=!0);var n=t.filter;void 0===n&&(n=function(t,e,n){return!0});var i=t.transformer;void 0===i&&(i=function(t){return t});var r=t.mutationTransformer;void 0===r&&(r=function(t){return t});var s=t.actionFilter;void 0===s&&(s=function(t,e){return!0});var a=t.actionTransformer;void 0===a&&(a=function(t){return t});var c=t.logMutations;void 0===c&&(c=!0);var u=t.logActions;void 0===u&&(u=!0);var l=t.logger;return void 0===l&&(l=console),function(t){var f=o(t.state);void 0!==l&&(c&&t.subscribe(function(t,s){var a=o(s);if(n(t,f,a)){var c=j(),u=r(t),h="mutation "+t.type+c;E(l,h,e),l.log("%c prev state","color: #9E9E9E; font-weight: bold",i(f)),l.log("%c mutation","color: #03A9F4; font-weight: bold",u),l.log("%c next state","color: #4CAF50; font-weight: bold",i(a)),M(l)}f=a}),u&&t.subscribeAction(function(t,n){if(s(t,n)){var i=j(),o=a(t),r="action "+t.type+i;E(l,r,e),l.log("%c action","color: #03A9F4; font-weight: bold",o),M(l)}}))}}};e.a=S}).call(e,n("DuR2"))},qspk:function(t,e){},rrSr:function(t,e){}});
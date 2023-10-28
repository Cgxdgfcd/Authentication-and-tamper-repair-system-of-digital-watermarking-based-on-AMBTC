<!-- 用户登录界面 -->
<template>
  <div id="login">
    <div class="bg"></div>
    <el-row class="main-container">
      <el-col :lg="8" :xs="16" :md="10" :span="10">
        <div class="top">
          <i class="el-icon-office-building"></i
          ><span class="title"><span style="font-size: 60px;"></span>基于AMBTC的数字水印的图像认证与修复系统</span>
        </div>
        <div class="bottom">
          <div class="container">
            <el-form
              :label-position="labelPosition"
              label-width="80px"
              :model="formLabelAlign"
			  style="margin-top: 15%;"
            >
              <el-form-item label="用户名" class="labelcolor">
                <el-input
                  v-model.number="formLabelAlign.username"
                  placeholder="请输入用户名"
                ></el-input>
              </el-form-item>
              <el-form-item label="密码" class="labelcolor">
                <el-input
                  v-model="formLabelAlign.password"
                  placeholder="请输入密码"
                  type="password"
                ></el-input>
              </el-form-item>
              <div class="submit">
                <el-button type="primary" class="row-login" @click="login()"
                  >登录</el-button
                >
              </div>
              <div class="options">
                <p class="find"><a href="javascript:;">找回密码</a></p>
                <div class="register">
                  <span>没有账号?</span>
                  <span><a href="javascript:;">去注册</a></span>
                </div>
              </div>
            </el-form>
          </div>
        </div>
      </el-col>
    </el-row>
    <el-row class="footer">
      <el-col>
        <p class="msg2"></p>
      </el-col>
    </el-row>
    <section class="remind">
      <span style="color: #fff;">欢迎!!</span>
    </section>
  </div>
</template>

<script>
import store from "@/vuex/store";
import axios from 'axios';
import { mapState } from "vuex";
export default {
  store,
  name: "login",
  data() {
    return {
      role: 2,
      labelPosition: "left",
      formLabelAlign: {
        username: "20154084",
        password: "123456",
      },
    };
  },
  methods: {
    //用户登录请求后台处理
    login() {
      console.log("登录操作执行-------");
	  const path = 'http://localhost:5000/ping';
	  axios.get(path)
	    .then((res) => {
	      console.log(res.data) ;
	    })
	    .catch((error) => {
	      // eslint-disable-next-line
	      console.error(error);
	    });
      this.$router.push({ path: "/mainControl" });
    },
    clickTag(key) {
      this.role = key;
    },
  },
  computed: mapState(["userInfo"]),
  mounted() {},
};
</script>

<style lang="scss" scoped>
.remind {
  border-radius: 4px;
  padding: 10px 20px;
  display: flex;
  position: fixed;
  right: 20px;
  bottom: 50%;
  flex-direction: column;
  color: #606266;
  border-left: 4px solid #409eff;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
.container {
  margin-bottom: 32px;
}
.container .el-radio-group {
  margin: 30px 0px;
}
a:link {
  color: #ff962a;
  text-decoration: none;
}
#login {
  font-size: 14px;
  color: #000;
  background-color: #fff;
}
.labelcolor /deep/ .el-form-item__label {
    text-align: left!important;
    vertical-align: middle;
    float: left;
    font-size: 14px;
    color: #fff;
    line-height: 40px;
    padding: 0 12px 0 0;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
}
#login .bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  overflow-y: auto;
  height: 100%;
  background: url("../../assets/img/login_bg2.jpg") center top / cover no-repeat;
  background-color: #b6bccdd1 !important;
  background-size:100% 100%;
  background-attachment:fixed;
}
#login .main-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
#login .main-container .top {
  margin-top: 20%;
  margin-bottom: 5%;
  font-size: 40px;
  color: #ff962a;
  font-weight: 700;
  display: flex;
  justify-content: center;
}
#login .top .el-icon-office-building {
  font-size: 80px;
  margin-right: 20px;
  margin-top: 5%;
}
#login .top .title {
  margin-top: 0px;
}
#login .bottom {
  display: flex;
  justify-content: center;
  // background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
#login .bottom .title {
  text-align: center;
  font-size: 30px;
}
.bottom .container .title {
  margin: 30px 0px;
}
.bottom .submit .row-login {
  width: 100%;
  background-color: #04468b;
  border-color: #04468b;
  margin: 20px 0px 10px 0px;
  padding: 15px 20px;
}
.bottom .submit {
  display: flex;
  justify-content: center;
}
.footer {
  margin-top: 50px;
  text-align: center;
}
.footer .msg1 {
  font-size: 18px;
  color: #fff;
  margin-bottom: 15px;
}
.footer .msg2 {
  font-size: 14px;
  color: #e3e3e3;
  margin-top: 70px;
}
.bottom .options {
  margin-top: 10px;
  margin-bottom: 20px;
  color: #ff962a;
  display: flex;
  justify-content: space-between;
}
.bottom .options > a {
  color: #ff962a;
}
.bottom .options .register span:nth-child(1) {
  color: #8c8c8c;
}
</style>

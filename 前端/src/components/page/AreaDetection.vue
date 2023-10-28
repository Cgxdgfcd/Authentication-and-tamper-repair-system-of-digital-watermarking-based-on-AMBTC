<template>
	<div
		class="AreaDetection"
		v-loading="is_processing"
		element-loading-text="正在处理中"
		element-loading-spinner="el-icon-loading"
		element-loading-background="rgba(0, 0, 0, 0.8)"
	>
		<el-row>
		  <el-col :span="7">
			  <el-card :body-style="{ padding: '10px' }" class="leftel-card">
          <div style="text-align: center;margin-bottom: 10px;">
            <span style="font-size: 28px;font-weight: 700;">待检测图片</span>
          </div>
          <el-image
            class="image"
            ref="preview"
            :src="pending_image_src[0]"
            :preview-src-list="pending_image_src">
          </el-image>
			    <div style="padding: 14px;">
			      <div style="text-align: center;">
              <input type="file" class="file_choose_input" name="file" id="file_choose_input" accept=".jpg, .jpeg, .png, .bmp" @input="chooseFileChanged()" hidden>
			        <el-button type="primary" class="button" @click="uploadImage()" round>上传图片</el-button>
              <el-button type="primary" class="button" @click="areaDetection()" round>区域检测</el-button>
            </div>
			    </div>
			  </el-card>
		  </el-col>

		  <el-col :span="3">
        <div style="height: 300px;margin-top: 65px;margin-left: 25%;">
          <el-steps direction="vertical" :active="step_process" finish-status="success" >
            <el-step title="上传图片"></el-step>
            <el-step title="区域检测"></el-step>
          </el-steps>
         <i class="el-icon-right"></i>
        </div>
		  </el-col>

		  <el-col :span="7">
			  <el-card :body-style="{ padding: '10px' }" class="rightel-card">
          <div style="text-align: center;margin-bottom: 10px;">
            <span style="font-size: 28px;font-weight: 700;">篡改区域对比图</span>
          </div>
			    <el-image
			    	class="image"
            ref="preview"
            :src="certification_image_src[0]"
            :preview-src-list="certification_image_src">
          </el-image>
			    <div style="padding: 14px;">
			      <div style="text-align: center;">
			        <el-button type="primary" class="button" round @click="preserveCertificationImage()">保存图片</el-button>
			      </div>
			    </div>
			  </el-card>
		  </el-col>

      <el-col :span="7">
        <el-card :body-style="{ padding: '10px' }" class="rightel-card">
          <div style="text-align: center;margin-bottom: 10px;">
            <span style="font-size: 28px;font-weight: 700;">篡改区域标识图</span>
          </div>
          <el-image
          	class="image"
              ref="preview"
              :src="identification_image_src[0]"
              :preview-src-list="identification_image_src"
          ></el-image>
          <div style="padding: 14px;">
            <div style="text-align: center;">
              <el-button type="primary" class="button" round @click="preserveIdentifiedImage()">保存图片</el-button>
            </div>
          </div>
        </el-card>
      </el-col>
		</el-row>

    <!-- 初代代码，保留待定

		<el-dialog
		  title="请选择待检测图片"
		  :visible.sync="dialogVisible1"
		  width="80%">
		  <div class="demo-image">
		    <div class="block" v-for="i in Math.ceil(tamperedPictureurls.length/6)" :key="i">
			  <el-row>
			    <el-col v-if="(i-1)*6+j<=tamperedPictureurls.length" :span="4" v-for="j in 6" :key="j">
					<el-card  shadow="hover" :class="[tamperedPictureischoose[(i-1)*6+j] ? 'selectedcard' : 'card']" >
					  <img
						  :src="getpath(tamperedPictureurls[(i-1)*6+j-1],'tampered/')"
						  class="image"
						  @click="SelecttamperedPicture((i-1)*6+j)"
					  />
					</el-card>
				</el-col>
			  </el-row>
		    </div>
		  </div>
		  <span slot="footer" class="dialog-footer">
		    <el-button @click="handleCancel()" round>取 消</el-button>
		    <el-button type="primary" @click="handleConfirm()" round>确认</el-button>
		  </span>
		</el-dialog>
   <el-dialog
      title="结果分析"
      :visible.sync="dialogVisible2"
      width="80%"
      @open="open()">
      <div >
        <div id="myChart" style="width:100%;height:430px;margin-top: 40px;"></div>
       </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleCancel()" round>取 消</el-button>
        <el-button type="primary" @click="handleConfirm()" round>确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      title="添加图片"
      :visible.sync="dialogVisible3"
      width="80%">
      <div class="addpicture"
      v-loading="addpictureloading"
      element-loading-text="正在上传中"
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
      >
      	<el-upload
      	  class="upload-demo"
      	  drag
      	  action=""
      	  :http-request="uploadSectionFile"
      	  multiple>
      	  <i class="el-icon-upload"></i>
      	  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      	  <div class="el-upload__tip" slot="tip">
      		  <el-select v-model="value" placeholder="请选择上传图片类型">
      		      <el-option
      		        v-for="item in options"
      		        :key="item.value"
      		        :label="item.label"
      		        :value="item.value">
      		      </el-option>
      		  </el-select>
      		  <span style="font-size: 18px;font-weight: 400;">非n*n的图片不允许上传!!</span>
      	  </div>
      	</el-upload>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleCancel()" round>取 消</el-button>
        <el-button type="primary" @click="handleConfirm()" round>确 定</el-button>
      </span>
    </el-dialog>
    -->

	</div>
</template>
<script>
import * as echarts from 'echarts'
import axios from 'axios';
export default {
  data() {
    return {
      is_processing:false,//控制加载
      step_process:0,//步骤条进度
      pending_image_src:[//待处理图片（原图）文件src
        this.$global.interfaceSetting.areaDetection.pendingImage,
      ],
      certification_image_src:[//篡改区域认证图片文件src
        this.$global.interfaceSetting.areaDetection.certificationImage,
      ],
      identification_image_src:[//原图篡改区域标识图文件src
        this.$global.interfaceSetting.areaDetection.identificationImage,
      ],
      identification_image_type:".png",//原图篡改区域标识图类型

      /* 初代代码，保留待定

        stepflag:0,
        loading:false,//控制加载
        addpictureloading:false,//控制加载
        dialogVisible1: false,//选择待检测图片
        dialogVisible2: false,//结果分析
        dialogVisible3: false,//添加图片
        CurrentSelectedPicture:null,//当前选中的图片
        currentDate: new Date(),//当前时间
        tamperedPictureischoose:[],//记录原图是否被选中以改变样式
        tamperedPictureurls:[],//待检测图片集
        tamperedPictureIndex:null,//待检测图片路径或编号
        srcList: [//用于预览、放大图片、注意格式、二维数组、由于数据格式要求、一个一维数组就储存一个地址、第一个为原图。。。
          [
            this.$global.interfaceSetting.areaDetection.pendingImage,
          ],
          [
            this.$global.interfaceSetting.areaDetection.callationImage,
          ],
          [
            this.$global.interfaceSetting.areaDetection.identificationImage,
          ]
        ],
        options: [
            // {
            //   value: '原图',
            //   label: '原图'
            // }, {
            //   value: '水印',
            //   label: '水印'
            // },
            {
              value: '待认证恢复图片',
              label: '待认证恢复图片'
            }],
        value: '待认证恢复图片',
        myChart: null,
        option: {
          title: {
               text: '检测结果'
          },
          tooltip: {},
          legend: {
              data:['所占图像百分比']
          },
          xAxis: {
              data: ["未篡改","已篡改"]
          },
          yAxis: {},
          series: [{
              name: '所占图像百分比',
              type: 'bar',
              data: [55, 45]
          }]
        },
      */
    };
  },
  /* 初代代码，保留待定

  watch:{
  	// 监听 option 更新
  	option: {
  		// 更新处理，也可以 handler(newVal，oldVal)
  		handler(newVal){
  			if(newVal){
  				this.myChart.setOption(newVal)
  			}
  		},
  		//关键,对象内部属性的监听(内部有数据更新，也进行对应的watch触发)
  		deep: true
  	},
  },
  mounted() {
    // this.drawBar();
  },
  created() {
    //特殊处理
    console.log(this.$cookies.get("addpictureflag"));
    if(this.$cookies.get("addpictureflag")==1){
      this.dialogVisible3=true;
    }
  	// this.InitDate();
  },
  */
  methods:{
    //上传原图
    uploadImage(){
      //模拟点击文件选择器
      document.getElementById("file_choose_input").click();
    },
    //篡改区域认证
    areaDetection(){
      //开启界面遮蔽
      this.is_processing = true;

      //获取需要提交的图片文件
      let files = document.getElementById("file_choose_input").files;

      //判断提交图片是否为空
      if(files.length == 0){
        //给出为空的提示
        this.$message({
          message: '请重新上传待检测图片!!',
          type: 'error'
        })

        //关闭界面遮蔽
        this.is_processing = false;
        return ;
      }

      //配置axios url以及参数
      const target_url = `http://localhost:5000/AreaDetection`;
      var formData = new window.FormData()
      formData.append('file',files[0])

      //向后端接口发送axios请求
      axios.post(target_url,formData,{headers:{'Content-Type':'application/x-www-form-urlencoded' }}, )
      .then((res) => {
        //使用Promise.all使其并行处理
        Promise.all([this.requestCertificationImageFile(res.data[0]),this.requestIdentificationImageFile(res.data[1])]).then((ans)=>{
          //给出成功提示
          this.$message({
            message: '篡改区域认证成功!!',
            type: 'success'
          })

          //更新步骤条
          this.step_process = 2;

          //关闭界面遮蔽
          this.is_processing = false;
        }).catch(reason => {
          //控制台输出报错提示
          console.log(reason);
          //给出错误提示
          this.$message({
            message: '数据异常，请重试!!',
            type: 'error'
          })
          //关闭界面遮蔽
          this.is_processing = false;
        });
      })
      .catch((error) => {
        //输出报错
        console.log(error)

        //嵌入失败
        this.$message({
          message: '嵌入失败!!',
          type: 'error'
        })
        //关闭界面遮蔽
        this.is_processing = false;
      });
    },
    //请求篡改区域认证图片
    requestCertificationImageFile(image_file){
      //获取后端文件名（篡改区域认证）
      let image = {
        url: `http://localhost:5000/getTargetImage`,
        method: 'get',
        responseType:"blob",
        params: {
          image_file
        }
      }

      //取得后端目标图片文件（篡改区域认证）
      axios.get(image.url, image).then((ans) => {
        //更新待处理图片src（篡改区域认证图片）
        this.certification_image_src = [];
        this.certification_image_src[0] = this.getObjectURL(ans.data);
      });
    },
    //请求篡改区域原图标识图片
    requestIdentificationImageFile(image_file){
      //获取后端文件名（篡改区域原图标识图）
      let image = {
        url: `http://localhost:5000/getTargetImage`,
        method: 'get',
        responseType:"blob",
        params: {
          image_file
        }
      }

      //取得后端目标图片文件（篡改区域原图标识图）
      axios.get(image.url, image).then((ans) => {
        //更新待处理图片src（篡改区域原图标识图）
        this.identification_image_src = [];
        this.identification_image_src[0] = this.getObjectURL(ans.data);

        //更新篡改区域原图标识图文件类型
        if(ans.data.type != null){
          this.identification_image_type = ans.data.type;
        }else this.identification_image_type = ".png";
      });
    },
    //下载保存篡改区域认证图片
    preserveCertificationImage(){
      //将图片的src属性作为URL地址
      var a = document.createElement('a')
      var event = new MouseEvent('click')
      a.download = "new_image.png" //'保存图片名称'
      a.href = this.certification_image_src[0];
      a.dispatchEvent(event)

      this.$message({ //开始保存图片提示
        message: '开始保存图片!!',
        type: 'success'
      })
    },
    //下载保存原图篡改区域标识图
    preserveIdentifiedImage(){
      //将图片的src属性作为URL地址
      var a = document.createElement('a')
      var event = new MouseEvent('click')
      a.download = "new_image" + this.identification_image_type //'保存图片名称'
      a.href = this.identification_image_src[0];
      a.dispatchEvent(event)

      this.$message({ //开始保存图片提示
        message: '开始保存图片!!',
        type: 'success'
      })
    },
    //监听input files值发生变化
    chooseFileChanged(){
      try{
        //读取input file的图片文件
        let upload_files = document.getElementById("file_choose_input").files;

        //对“没有选择图片文件，upload_files无元素”情况进行判断
        if(upload_files.length == 0){
          //更新步骤条
          this.step_process = 0;
          return ;
        }

        new Promise((resolve,reject)=>{
          //判断图片尺寸是否为n*n
          var temp_img = new Image();
          temp_img.src = this.getObjectURL(upload_files[0]);
          temp_img.onload = ()=>{
            if(temp_img.height != temp_img.width){
              //提示上传失败
              this.$message({
                message: '请重新上传n*n大小的图片!!',
                type: 'error'
              })
              reject();
            }else{
              resolve();
            }
          }
        }).then((resolve,reject)=>{
          //更新待处理图片src
          this.pending_image_src = [];
          this.pending_image_src[0] = this.getObjectURL(upload_files[0]);

          //更新篡改区域认证图片，置为初始状态
          this.certification_image_src = [];
          this.certification_image_src[0] = this.$global.interfaceSetting.areaDetection.certificationImage;

          //更新篡改区域标识图片，置为初始状态
          this.identification_image_src = [];
          this.identification_image_src[0] = this.$global.interfaceSetting.areaDetection.identificationImage;

          //更新步骤条
          this.step_process = 1;

          //提示上传成功
          this.$message({
            message: '图片上传成功!!',
            type: 'success'
          })
        }).catch(error => {
          return ;
        })
      }catch(e){
        //提示上传失败
        this.$message({
          message: '图片上传失败!!',
          type: 'error'
        })
      }
    },
    //获取file类型的url
    getObjectURL(file) {
        var url = null ;
        //针对不同的浏览器执行不同的js函数
        if (window.createObjectURL!=undefined) { // basic
            url = window.createObjectURL(file) ;
        } else if (window.URL!=undefined) { // mozilla(firefox)
            url = window.URL.createObjectURL(file) ;
        } else if (window.webkitURL!=undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file) ;
        }
        return url ;
    },

    /* 初代代码，保留待定

      //自定义上传
      async uploadSectionFile(param){
        this.stepflag=1;
        this.addpictureloading=true
        console.log(param)
        var fileObj = param.file;
        var form = new FormData();
        console.log(fileObj)
         // 文件对象
        form.append("file", fileObj);
        var _this=this;
        new Promise(function (resolve, reject) {
            // 定义 filereader对象
          let reader = new FileReader()
            reader.readAsDataURL(fileObj)
            reader.onload = e=>{
                const img = e.target.result;
                const image = new Image()
                image.src=img
                image.onload = _=>{
              let width = image.width
              let height= image.height
              if(width!=height){
                _this.$message({ //成功修改提示
                  message: '非n*n的图片不允许上传!!',
                  type: 'error'
                })
                resolve(false);
              }else{
                _this.$axios.post(`http://localhost:5000/addpicture/${_this.value}`,form).then(res => {
                  param.onSuccess(res)
                  console.log(res)
                  _this.$message({ //成功修改提示
                    message: '上传成功!!',
                    type: 'success'
                  })
                  _this.dialogVisible3=false;
                  _this.addpictureloading=false;
                  _this.tamperedPictureIndex=fileObj.name;
                  _this.srcList[0][0]=_this.getpath(fileObj.name,"tampered/")
                }).catch(({err}) => {
                  param.onError(err)
                  _this.$message({ //成功修改提示
                    message: '上传失败!!',
                    type: 'success'
                  })
                  _this.addpictureloading=false;
                })
                resolve(true);
              }
                }
            }
        }).then(res=>{
          return res;
        });
      },
      //上传图片
      uploadimage(){
        if(this.$cookies.get("addpictureflag")==0){
          this.$cookies.set("addpictureflag", 1);
          this.dialogVisible3=true;
        }else{
          this.flush();
        }
      },
      //刷新界面
      flush(){
        this.$router.go(0);
      },
      open() {
        const t = this;
          setTimeout(() => {
            //  执行echarts画图方法
            t.drawBar();
          }, 0);
      },
      drawBar() {
        // 基于准备好的dom，初始化echarts实例
        // 全局使用 echarts
        // this.myChart = this.$echarts.init(document.getElementById('myChart'))
        // 调用局部的 echarts
        this.myChart = echarts.init(document.getElementById('myChart'))
        // 绘制图表
        this.myChart.setOption(this.option);

        // 设置该 chart 的 resize 方法
        window.addEventListener("resize", this.myChart.resize)
      },
      getpath(path,type){
          return path ? require('D:/2023-2-6/image/'+type+ path) : '';//path不为null就返回对应的路径
      },
      InitDate(){
        //加载待检测图片
        let files = require.context('D:/2023-2-6/image/tampered/', true)
        let i=0;
        // 遍历输出匹配结果
        files.keys().forEach(path=> {
          let paths=path.split('./')
          let newpath=paths[1]
          this.tamperedPictureurls[i]=newpath;
          i++;
        })
        for(let i=0;i<=this.tamperedPictureurls.length;i++){
            this.tamperedPictureischoose[i]=false;
        }
      },
      //选择原图
      SelecttamperedPicture(flag){
        this.stepflag=1;
        if(this.CurrentSelectedPicture!=null){
          this.tamperedPictureischoose[this.CurrentSelectedPicture]=false;
        }
        this.tamperedPictureischoose[flag]=true;
        this.CurrentSelectedPicture=flag;
        this.tamperedPictureIndex=this.tamperedPictureurls[flag-1];
        this.srcList[0][0]=this.getpath(this.tamperedPictureIndex,"tampered/")
        //起刷新效果、原因未知。。。
        this.dialogVisible1 = false;
        this.dialogVisible1 = true;

      },
      handleCancel(){
        this.dialogVisible1 = false;
        this.dialogVisible2 = false;
        this.dialogVisible3 = false;
      },
      handleConfirm(){
        this.dialogVisible1 = false;
        this.dialogVisible2 = false;
        this.dialogVisible3 = false;
      },
      // 保存篡改区域认证图片
      preserveCertificationImage(){
        // 将图片的src属性作为URL地址
        var a = document.createElement('a')
        var event = new MouseEvent('click')
        a.download = "new_image.png" // '保存图片名称'
        a.href = this.srcList[1][0]
        a.dispatchEvent(event)

        this.$message({ //开始保存图片提示
          message: '开始保存图片!!',
          type: 'success'
        })
      },
      // 保存原图篡改区域标识图片
      preserveIdentifiedImage(){
        // 将图片的src属性作为URL地址
        var a = document.createElement('a')
        var event = new MouseEvent('click')
        a.download = "new_image.png" // '保存图片名称'
        a.href = this.srcList[2][0]
        a.dispatchEvent(event)

        this.$message({ //开始保存图片提示
          message: '开始保存图片!!',
          type: 'success'
        })
      },
      //区域检测
      AreaDetection(){
        if(this.tamperedPictureIndex==null){
          this.$message({ //成功修改提示
            message: '请选择待检测图片!!',
            type: 'error'
          })
          return;
        }
        this.loading=true;
        let tamperedPicturepath={
          path:'D:/2023-2-6/image/tampered/'+this.tamperedPictureIndex
        };
        const path = `http://localhost:5000/AreaDetection`;
        axios.post(path,tamperedPicturepath)
          .then((res) => {
            this.stepflag=2;
            this.$message({ //成功修改提示
              message: '检测成功!!',
              type: 'success'
            })
            //嵌入的图片以原图命名
            let path=res.data;
            console.log(path)
            this.srcList[1][0]=require("D://2023-2-6//flask//Digital_Watermark_Embedding_And_Tampering_Repair_System//cache//"+path[0])
            this.srcList[2][0]=require("D://2023-2-6//flask//Digital_Watermark_Embedding_And_Tampering_Repair_System//cache//"+path[1])
            this.loading=false;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.log(error)
            this.$message({ //成功修改提示
              message: '检测失败!!',
              type: 'error'
            })
            this.loading=false;
          });
      }
    */


  }
}
</script>
<style scoped>
	.AreaDetection{
    height: 100%;
    background-color: rgb(239, 239, 239);
	}
  .AreaDetection /deep/ .el-upload-dragger{
  			width: 650%;
  	    margin-top: 10%;
  	    margin-left: 1%;
  }
	.el-icon-right {
	  font-size: 120px;
	  padding-top: 50px;
	  margin-right: 10px;
	}
  .time {
    font-size: 20px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    font-size: 18px;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }

  .clearfix:after {
      clear: both
  }
  .selectedcard{
        padding: 2px;
        background-color: cornflowerblue;
  }
  .AreaDetection /deep/ .el-card__body {
      padding: 0px;
  }
  .card{
	  padding: 10px;
  }
  .AreaDetection /deep/ .el-icon-loading{
	  font-size: 70px;
  }
  .AreaDetection /deep/ .rightel-card {
      border: 1px solid #EBEEF5;
      background-color: #FFF;
      color: #303133;
      -webkit-transition: .3s;
      transition: .3s;
      width: 100%;
      margin-top: 5%;
  }
  .AreaDetection /deep/ .leftel-card {
      border: 1px solid #EBEEF5;
      background-color: #FFF;
      color: #303133;
      -webkit-transition: .3s;
      transition: .3s;
      width: 100%;
      margin-left: 5%;
      margin-top: 5%;
  }
</style>

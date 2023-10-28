<template>
	<div
		class="embedwatermark"
		v-loading="is_processing"
		element-loading-text="正在处理中"
		element-loading-spinner="el-icon-loading"
		element-loading-background="rgba(0, 0, 0, 0.8)"
	>
		<el-row>
		  <el-col :span="11">
			  <el-card :body-style="{ padding: '10px' }" class="leftel-card">
          <div style="text-align: center;margin-bottom: 10px;">
            <span style="font-size: 28px;font-weight: 700;">原图</span>
          </div>
          <el-image
            class="image"
            ref="preview"
            :src="pending_image_src[0]"
            :preview-src-list="pending_image_src"
          ></el-image>
          <div style="padding: 14px;">
            <div style="text-align: center;">
              <input type="file" class="file_choose_input" name="file" id="file_choose_input" accept=".jpg, .jpeg, .png, .bmp" @input="chooseFileChanged()" hidden>
              <el-button type="primary" class="button" @click="uploadImage()" round>上传图片</el-button>
              <el-button type="primary" class="button" @click="embedWatermark()" round>嵌入水印</el-button>
            </div>
          </div>
			  </el-card>
		  </el-col>

		  <el-col :span="2">
        <div style="height: 300px;margin-top: 100px;">
          <el-steps direction="vertical" :active="step_process" finish-status="success" >
            <el-step title="上传原图"></el-step>
            <el-step title="嵌入水印"></el-step>
          </el-steps>
         <i class="el-icon-right"></i>
        </div>
		  </el-col>

		  <el-col :span="11">
			  <el-card :body-style="{ padding: '10px' }" class="rightel-card">
			    <div style="text-align: center;margin-bottom: 10px;">
			      <span style="font-size: 28px;font-weight: 700;">嵌入水印图</span>
			    </div>
          <el-image
			    	class="image"
            ref="preview"
            :src="embed_image_src[0]"
            :preview-src-list="embed_image_src"
			    ></el-image>
			    <div style="padding: 14px;">
			      <div style="text-align: center;">
			        <el-button type="primary" class="button" round @click="preserveEmbededImage()">保存图片</el-button>
			      </div>
			    </div>
			  </el-card>
		  </el-col>
		</el-row>
    <!-- 初代代码，保留待定
      <el-dialog
        title="请选择要嵌入的水印图片"
        :visible.sync="choose_pending_image_dialog_visible"
        width="80%">
        <div class="demo-image">
          <div class="block" v-for="i in Math.ceil(EmbedWatermarkurls.length/6)" :key="i">
          <el-row>
            <el-col v-if="(i-1)*6+j<=EmbedWatermarkurls.length" :span="4" v-for="j in 6" :key="j">
            <el-card  shadow="hover" :class="[EmbedWatermarkischoose[(i-1)*6+j] ? 'selectedcard' : 'card']" >
              <img
                :src="getpath(EmbedWatermarkurls[(i-1)*6+j-1],'watermark/')"
                class="image"
                @click="SelectWatermark((i-1)*6+j)"
              />
            </el-card>
          </el-col>
          </el-row>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="handleCancel()" round>取 消</el-button>
          <el-button type="primary" @click="DetermineEmbedding()" round>确认嵌入</el-button>
        </span>
      </el-dialog>
    -->
    <!-- 初代代码，保留待定
      <el-dialog
        title="请选择原图"
        :visible.sync="dialogVisible2"
        width="80%">
        <div class="demo-image">
          <div class="block" v-for="i in Math.ceil(OriginalPictureurls.length/6)" :key="i">
          <el-row>
            <el-col v-if="(i-1)*6+j<=OriginalPictureurls.length" :span="4" v-for="j in 6" :key="j">
            <el-card  shadow="hover" :class="[OriginalPictureischoose[(i-1)*6+j] ? 'selectedcard' : 'card']" >
              <img
                :src="getpath(OriginalPictureurls[(i-1)*6+j-1],'original/')"
                class="image"
                @click="SelectOriginalImage((i-1)*6+j)"
              />
            </el-card>
          </el-col>
          </el-row>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="handleCancel()" round>取 消</el-button>
          <el-button type="primary" @click="handleConfirm()" round>确 定</el-button>
        </span>
      </el-dialog>
    -->
    <!-- 初代代码，保留待定
      <el-dialog
        title="添加图片"
        :visible.sync="choose_pending_image_dialog_visible"
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
import axios from 'axios';
export default {
  data() {
    return {
      is_processing:false,//控制加载
      step_process:0,//步骤条进度
      pending_image_src:[//待处理图片（原图）文件src
        this.$global.interfaceSetting.embedWatermark.originImage,
      ],
      embed_image_src:[//已嵌入水印后图片文件src
        this.$global.interfaceSetting.embedWatermark.embedImage,
      ],
      embed_image_type:".png",//已嵌入水印后图片类型

      /* 初代代码，保留待定

        stepflag:0,
        options: [
            {
              value: '原图',
              label: '原图'
            },
        ],
        value: '原图',
        fileReader: '',
        flag:true,
        addpictureloading:false,//控制加载
        dialogVisible1: false,//嵌入水印
        CurrentSelectedPicture:null,//当前选中的图片
        dialogVisible2: false,//选择原图
        dialogVisible3: false,//添加图片
        currentDate: new Date(),//当前时间
        ischoose:[],//记录嵌入水印和原图是否被选中以改变样式
        EmbedWatermarkischoose:[],//记录嵌入水印是否被选中以改变样式
        OriginalPictureischoose:[],//记录原图是否被选中以改变样式
        EmbedWatermarkurls:[],//水印图片集
        OriginalPictureurls:[],//原图图片集
        OriginalPictureIndex:null,//原图路径或编号
        EmbedWatermarkIndex:null,//嵌入水印图路径或编号
        srcList: [//用于预览、放大图片、注意格式、二维数组、由于数据格式要求、一个一维数组就储存一个地址、第一个为原图。。。
          [
            this.$global.interfaceSetting.embedWatermark.originImage,
          ],
          [
            this.$global.interfaceSetting.embedWatermark.embedImage,
          ]
        ],
      */
    };
  },
  methods:{
    //上传原图
    uploadImage(){
      //模拟点击文件选择器
      document.getElementById("file_choose_input").click();
    },
    //嵌入水印
    embedWatermark(){
      //开启界面遮蔽
      this.is_processing = true;

      //获取需要提交的图片文件
      let files = document.getElementById("file_choose_input").files;

      //判断提交图片是否为空
      if(files.length == 0){
        //给出为空的提示
        this.$message({
          message: '请重新上传原图!!',
          type: 'error'
        })

        //关闭界面遮蔽
        this.is_processing = false;
        return ;
      }

      //配置axios url以及参数
      const target_url = `http://localhost:5000/EmbedWatermark`;
      var formData = new window.FormData()
      formData.append('file',files[0])

      //向后端接口发送axios请求
      axios.post(target_url,formData,{headers:{'Content-Type':'application/x-www-form-urlencoded' }}, )
      .then((res) => {
        //获取后端文件名
        let image_file = res.data;
        let embed_image = {
          url: `http://localhost:5000/getTargetImage`,
          method: 'get',
          responseType:"blob",
          params: {
            image_file
          }
        }

        //取得后端目标图片文件
        axios.get(embed_image.url, embed_image).then((ans) => {
          //更新待处理图片src
          this.embed_image_src = [];
          this.embed_image_src[0] = this.getObjectURL(ans.data);

          //更新嵌入水印图片文件类型
          if(ans.data.type != null){
            this.embed_image_type = ans.data.type;
          }else this.embed_image_type = ".png";
        });

        //给出成功提示
        this.$message({
          message: '水印嵌入成功!!',
          type: 'success'
        })

        //更新步骤条
        this.step_process = 2;

        //关闭界面遮蔽
        this.is_processing = false;
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
    //保存嵌入水印后的图片
    preserveEmbededImage(){
      //获取文件后缀
      var file_name = this.embed_image_src[0];
      var suffix = file_name.substring(file_name.lastIndexOf("."));

      //将图片的src属性作为URL地址
      var a = document.createElement('a')
      var event = new MouseEvent('click')
      a.download = "new_image" + this.embed_image_type //'保存图片名称'
      a.href = this.embed_image_src[0];
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

          //更新嵌入水印图片，置为初始状态
          this.embed_image_src = [];
          this.embed_image_src[0] = this.$global.interfaceSetting.embedWatermark.originImage;

          //更新步骤条
          this.step_process = 1;

          //提示上传成功
          this.$message({
            message: '图片上传成功!!',
            type: 'success'
          })
        }).catch(error =>{
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
        // console.log(param)
        var fileObj = param.file;
        var form = new FormData();
        // console.log(fileObj)
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
                    _this.$message({
                      message: '非n*n的图片不允许上传!!',
                      type: 'error'
                    })
                    resolve(false);
                  }else{
                    _this.$axios.post(`http://localhost:5000/addpicture/${_this.value}`,form).then(res => {
                      param.onSuccess(res)
                      _this.$message({ //成功修改提示
                        message: '上传成功!!',
                        type: 'success'
                      })
                      _this.OriginalPictureIndex=fileObj.name;
                      _this.srcList[0][0]=_this.getpath(fileObj.name,"original/")
                      _this.dialogVisible3=false;
                      _this.addpictureloading=false;
                    }).catch(({err}) => {
                      param.onError(err)
                      console.log(err)
                      _this.$message({ //成功修改提示
                        message: '上传失败!!',
                        type: 'error'
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
      getpath(path,type){
          return path ? require('D:/2023-2-6/image/'+type+ path) : '';//path不为null就返回对应的路径
      },
      InitDate(){
        //加载水印图片
        let files = require.context('D:/2023-2-6/image/watermark/', true)
        let i=0;
        // 遍历输出匹配结果
        files.keys().forEach(path=> {
          let paths=path.split('./')
          let newpath=paths[1]
          this.EmbedWatermarkurls[i]=newpath;
          i++;
        })
        for(let i=0;i<=this.EmbedWatermarkurls.length;i++){
            this.EmbedWatermarkischoose[i]=false;
        }
        //加载原图图片
        files = require.context('D:/2023-2-6/image/original/', true)
        i=0;
        // 遍历输出匹配结果
        files.keys().forEach(path=> {
            let paths=path.split('./')
            // let newpath='@/assets/img/'+paths[1]
          let newpath=paths[1]
            this.OriginalPictureurls[i]=newpath;
            i++;
        })
        for(let i=0;i<=this.OriginalPictureurls.length;i++){
            this.OriginalPictureischoose[i]=false;
        }
      },
      //选择水印图片
      SelectWatermark(flag){//flag用于确定选择的图片编号
        this.stepflag=2;
        //初始化处理
        if(this.CurrentSelectedPicture!=null){
          this.EmbedWatermarkischoose[this.CurrentSelectedPicture]=false;
        }
        this.EmbedWatermarkischoose[flag]=true;
        this.CurrentSelectedPicture=flag;
        this.EmbedWatermarkIndex=this.EmbedWatermarkurls[flag-1];
        //起刷新效果、原因未知。。。
        this.dialogVisible1 = false;
        this.dialogVisible1 = true;
      },
      //选择原图
      SelectOriginalImage(flag){
        this.stepflag=1;
        if(this.CurrentSelectedPicture!=null){
          this.OriginalPictureischoose[this.CurrentSelectedPicture]=false;
        }
        this.OriginalPictureischoose[flag]=true;
        this.CurrentSelectedPicture=flag;
        this.OriginalPictureIndex=this.OriginalPictureurls[flag-1];
        this.srcList[0][0]=this.getpath(this.OriginalPictureIndex,"original/")
        //起刷新效果、原因未知。。。
        this.dialogVisible2 = false;
        this.dialogVisible2 = true;
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

      //嵌入水印
      DetermineEmbedding(){
        this.dialogVisible1 = false;
        this.dialogVisible2 = false;
        if(this.OriginalPictureIndex==null){
          this.$message({ //成功修改提示
            message: '请选择原图!!',
            type: 'error'
          })
          return;
        }
        let OriginalPicturepath={
          path:'D:/2023-2-6/image/original/'+this.OriginalPictureIndex
        };
        let path = `http://localhost:5000/EmbedWatermark`;
        this.loading=true;
        axios.post(path,OriginalPicturepath)
          .then((res) => {
            console.log(res)
            this.stepflag=3;
            this.$message({ //成功修改提示
              message: '嵌入成功!!',
              type: 'success'
            })
            //嵌入的图片以原图命名
            let path=res.data;
            console.log(path)
            this.srcList[1][0]=require("D://2023-2-6//flask//Digital_Watermark_Embedding_And_Tampering_Repair_System//cache//"+path)
            this.loading=false;
          })
          .catch((error) => {
            console.log(error)
            // eslint-disable-next-line
            this.$message({ //成功修改提示
              message: '嵌入失败!!',
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
  .embedwatermark /deep/ .el-upload-dragger{
    width: 650%;
    /* height: 30%; */
    margin-top: 10%;
    margin-left: 1%;
  }
	.embedwatermark{
      height: 100%;
      background-color: rgb(239, 239, 239);
	}
	.el-icon-right {
	  font-size: 120px;
	  padding-top: 80px;
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

  .file_choose_input{

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
  .embedwatermark /deep/ .el-card__body {
      padding: 0px;
  }
  .card{
	  padding: 10px;
  }
  .embedwatermark /deep/ .el-icon-loading{
	  font-size: 70px;
  }
  .embedwatermark /deep/ .rightel-card {
      border: 1px solid #EBEEF5;
      background-color: #FFF;
      color: #303133;
      -webkit-transition: .3s;
      transition: .3s;
      width: 75%;
      margin-left: 10%;
      margin-top: 3%;
  }
  .embedwatermark /deep/ .leftel-card {
      border: 1px solid #EBEEF5;
      background-color: #FFF;
      color: #303133;
      -webkit-transition: .3s;
      transition: .3s;
      width: 75%;
      margin-left: 15%;
      margin-top: 3%;
  }
</style>

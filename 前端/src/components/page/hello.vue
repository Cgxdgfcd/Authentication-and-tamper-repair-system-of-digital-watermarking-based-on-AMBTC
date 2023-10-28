<template>
   <div id="hello">
	    <el-carousel :interval="5000" arrow="always">
	   	 <el-carousel-item>
	   			<img src="../../assets/img/世界地球日.png" class="image" @click="flush()">
	   	 </el-carousel-item>
			 <el-carousel-item>
			 	  <img src="../../assets/img/EmbedWatermark.png" class="image" @click="toEmbedWatermark()">
			 </el-carousel-item>
			 <el-carousel-item>
			 	  <img src="../../assets/img/AreaDetection.png" class="image" @click="toAreaDetection()">
			 </el-carousel-item>
			 <el-carousel-item>
			 	  <img src="../../assets/img/RestorePicture.png" class="image" @click="toRestorePicture()">
			 </el-carousel-item>
	   	</el-carousel>
   </div>
</template>

 <script>
export default {
		 data() {
		   return {

		   };
		 },
		 methods:{
		 		toEmbedWatermark(){
		 			this.$router.push({ path: "/EmbedWatermark" });
          //设置全局参数
          this.$cookies.set("addpictureflag", 0);
          console.log(this.$cookies.get("addpictureflag"))
		 		},
		 		toAreaDetection(){
		 			this.$router.push({ path: "/AreaDetection" });
          //设置全局参数
          this.$cookies.set("addpictureflag", 0);
          console.log(this.$cookies.get("addpictureflag"))
		 		},
		 		toRestorePicture(){
		 			this.$router.push({ path: "/RestorePicture" });
          //设置全局参数
          this.$cookies.set("addpictureflag", 0);
          console.log(this.$cookies.get("addpictureflag"))
		 		},
        flush(){
          this.$router.go(0);
        }
		 }
	 }
 </script>

 <style lang="scss" scoped>
 .image {
   cursor: pointer;
   top: 0;
   left: 0;
   width: 100%;
   overflow-y: auto;
   height: 100%;
   background-color: #b6bccdd1 !important;
   background-size:100% 100%;
   background-attachment:fixed;
 }
 #hello /deep/ .el-carousel__container {
     position: relative;
     height: 680px;
 }
.el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
 </style>

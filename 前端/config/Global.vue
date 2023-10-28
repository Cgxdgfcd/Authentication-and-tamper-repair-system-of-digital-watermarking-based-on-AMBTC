<script>
  //系统工作路径配置
  const fileWorkingPath = {
    fileDefaultWorkingCache : "D:/2023-2-6/flask/Digital_Watermark_Embedding_And_Tampering_Repair_System/cache",//默认工作存储路径
    fileDefaultSavePath : "D:/2023-2-6/save_file"//文件默认保存路径
  }
  //界面图片配置
  const interfaceSetting = {
    // 嵌入水印功能界面默认图
    embedWatermark:{
      originImage:require('../src/assets/img/background1.png'),//原图
      embedImage:require('../src/assets/img/background1.png')//待上传图片
    },
    // 图像认证
    areaDetection:{
      pendingImage:require('../src/assets/img/background1.png'),//待检测图片
      certificationImage:require('../src/assets/img/background1.png'),//篡改区域对比图
      identificationImage:require('../src/assets/img/background1.png')//篡改区域识别图
    },
    // 篡改恢复
    restorePicture:{
      pendingImage:require('../src/assets/img/background1.png'),//待恢复图片
      restoreImage:require('../src/assets/img/background1.png')//已恢复图片
    }
  }

  export default
  {
    fileWorkingPath,
    interfaceSetting
  }
</script>

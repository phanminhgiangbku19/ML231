<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
      <p :style="messageStyle">{{messageContent}}</p>
    </template>
    <div class="form__group field">
      <input v-model="videoUrl" type="input" class="form__field" placeholder="Name" name="name" id='name' required />
      <label for="name" class="form__label">Video URL</label>
    </div>
    <br>
    <button @click="process()" class="button-85" role="button">Process</button>
  </WelcomeItem>
  <div v-for="(src, index) in imageSrcs" :key="index">
    <img :src="`http://10.229.91.59:8080/static/${folder}/` + src">
  </div>
</template>

<script>
  import axios from 'axios';
  const imageListApi = 'http://10.229.91.59:8080/api/get-list-filenames?folder=';
  const videoApi = 'http://10.229.91.59:8080/api/detect?query=';
export default {
  data() {
    return {
      messageStyle: '',
      messageContent: '',
      imageSrcs: [],
      folder: ''
    };
  },
  methods: {
    process() {
      // this.messageStyle = 'color: red';
      // this.messageContent = 'Bad video!';})
      axios({
          method: "get",
          url: videoApi + this.videoUrl,
        })
        .then(response => {
          this.folder = response.data.file_name;
          this.getImages();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },

    async getImages() {
      await axios({
          method: "get",
          url: imageListApi + this.folder,
        })
        .then(response => {
          this.imageSrcs = response.data;
          if (this.imageSrcs.length != 0) {
            this.messageStyle = 'color: red';
            this.messageContent = 'Không ổn rồi bạn ơi!';
          } else {
            this.messageStyle = 'color: red';
            this.messageContent = 'Ok!'
          }
        })
        .catch(error => {
          console.error('Error getting images:', error);
        });
    }
  },
};
</script>

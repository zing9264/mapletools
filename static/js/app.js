const { createApp } = Vue;

createApp({
  data() {
    return {
      form: {
        target_count: null,
        scroll_cost: null,
        success_rate: null,
        max_attempts: null
      },
      lastResult: null
    }
  },
  methods: {
    async submit() {
      const resp = await axios.post('/api/simulate', this.form);
      this.lastResult = resp.data;
      // 表單不清空，可以繼續修改重送
    }
  }
}).mount('#app');

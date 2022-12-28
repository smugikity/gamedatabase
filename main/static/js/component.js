export default {
  props: ['value'],
  template: `
    <h3>{{value}}</h3> 
  `,
  created() {
    // props are exposed on `this`
    console.log(this.value)
  }
}
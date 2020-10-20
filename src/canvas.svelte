<script>
  let canvas, ctx;
  import { onMount } from "svelte";
  onMount(() => {
  canvas.width=5000
    ctx = canvas.getContext("2d");
    let f_ex1 = x => {
      return ((-x * x + 1) * 3) / 4;
    };
    let f_ex2 = x => {
      if (x > 0) {
        return -x + 1;
      } else if (x < 0) {
        return x + 1;
      }
    };
    //
    let a = [
      ...Array(20)
        .fill(0)
        .map((e, i) => (i > 10 ? 1 : 0)),
      ...Array(20)
        .fill(0)
        .map((e, i) => (i < 10 ? 1 : 0))
    ];
    let constructCont = (a,color) => {
      let r = 8;
      let calc = x => {
        let s = 0;
        let start = Math.ceil(x - r);
        let end = Math.floor(x + r);
        for (let i = start; i <= end; i++) {
          let realI = i - 1;
          let value = a[realI] * f_ex2((x - i) / r);
          s += value;
        }
        return s;
      };
      let values = [];
      for (let x = 0; x < a.length; x += 0.01) {
        values.push(calc(x));
      }
      values = values.filter(e => !isNaN(e));
      let vmax = Math.max(...values)+.10; // for margin
      console.log(vmax);
      ctx.fillStyle = color
      values.map((e, i) => {
        ctx.fillRect(
          (i / values.length) * canvas.width,
          canvas.height - ( (e - 0.1) / vmax) * canvas.height -10,
          5,
          5
        );
      });
    };
    //constructCont(a);
    let rand = Array(400).fill(0).map(e=>Math.random())
    constructCont(rand,"black")
    // zooming in on the rand
    let rand2 = Array(400).fill(0).map((e,i)=> {
      return rand[Math.floor(i/4)]
    })
    constructCont(rand2,"red")
  });
</script>

<canvas bind:this={canvas} />

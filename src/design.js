let debug = true
let logit = (...args)=> {
    if (debug) {
        args.map(e=> console.log(e))
    }
}
// line is an adaptor of sorts I guess
let Line = () => ({
    line(ps, pe) {
        this.ctx.beginPath()
        this.ctx.moveTo(ps.x, ps.y)
        this.ctx.lineTo(pe.x, pe.y)
        this.ctx.closePath()
        this.ctx.stroke()
    }
})
// ?? what would be a good example of graphics using the decorator pattern, 
// benefits, are similar to inheritance but more flexible, 
// similar to adapter, but modifications done at runtime. maybe geometries are decoratable?
// maybe do decorations on the triangle with other attributes we might want to control? start with 
// start with example

let Beverage =()=> ({
    total:0,
    desc:"",
    getDescription() {
        return `drink consists of ${this.desc}`
    },
    cost() {
        return `cost of drink is  ${this.total}`
    }
})
// tihs inheritance is the only step that requires it in decoration
let DR = ()=> ({
   ...Beverage(),
})

let MochaWrap=(BaseDrink) => ({
    total:.5,
    desc:"mocha",
    BD:BaseDrink,
    getDescription() {
        this.BD.desc += this.desc
        return this.BD.getDescription()
    },
    cost() {
        this.BD.total += this.total
        return this.BD.cost()
    }
})

let IcecreamScoop = (BaseDrink)=>({
    BD:BaseDrink,
    total:3.2,
    desc:"ice cream ",
    getDescription() {
        return this.BD.getDescription() + ","+ this.desc
    },
    cost() {
        this.BD.total += this.total
        return this.BD.cost()
    }
})


let Point = ({ x, y }) => ({
    x, y
})
// make a leaf class
let SimpleGeometry = () => ({
    lines: [],
    addLine(pt) {
        this.lines.push(pt)
    },
    drawShape() {
        return [...this.lines]
    }
})
let Triangle = ({ center, size } = {}) => {
    if (center != undefined && size != undefined) {
        let points = []
        for (let i = 0; i < 4; i++) {
            points.push(Point({
                x: Math.cos(i / 3 * Math.PI * 2) * size + center,
                y: Math.sin(i / 3 * Math.PI * 2) * size + center
            }))
        }
        logit(points)
        let sg = SimpleGeometry()
        sg.lines = points
        return sg
    } else {
        logit("didn't get args")
    }
}
// drawShape will get called on all its components
// this will be a composite
let CompoundGeometry = () => ({
    shapes: [],
    drawShape() {
        let final = []
        for (let s of this.shapes) {
            final = [...final, ...s.drawShape()]
        }
        return final
    }
})
let Listener = () => ({
    objects: [],
    change(ob) {
        for (let o of this.objects) {
            o.response(ob)
        }
    }
})
let ClickDetect = (element, listener) => {
    let x = 0
    let y = 0
    element.addEventListener("click", (e) => {
        let bbox = element.getBoundingClientRect()
        logit("got click on ", element)
        x = e.clientX - bbox.left
        y = e.clientY - bbox.top
        listener.change({ x, y })
    })
}
let Graphic = (canvas) => ({
    canvas,
    ctx: canvas.getContext("2d"),
    ...Line(),

    fromOrigin(pe) {
        return this.line({ x: 0, y: 0 }, pe)
    },
    response(ob) {
        this.fromOrigin(ob)
    }
})
let ClickableGraphicBuilder = (canvas) => ({
    build() {
        let graphic = Graphic(canvas)
        let listener = Listener()
        listener.objects.push(graphic)
        ClickDetect(canvas, listener)
        return graphic
    }
})



// interface is that we can provide text output
// how to share canvas without making it global?
let Main = () => ({
    text: "",
    setup(canvas) {
        canvas.height = window.innerHeight
        canvas.width = window.innerWidth
        let geo = CompoundGeometry()
        for (let i = 0; i < 80; i++) {
            let t = Triangle({ center: Math.random()*canvas.height, size: Math.random()*200})
            logit(t)
            geo.shapes.push(t)
        }
        logit(geo)
        let g1 = ClickableGraphicBuilder(canvas).build()
        logit(g1)
        let points = geo.drawShape()
        for (let i = 0; i < points.length -1; i++) {
            let ps = points[i ]
            let pe = points[(i + 1)]
            logit(ps, pe)
            if ((i+1)%4 != 0) {
                g1.line(ps, pe)
            }
        }
        // do the beverage stuff
        let mochWithIceCream = IcecreamScoop(MochaWrap(DR()))
        logit("drink total is ",mochWithIceCream.cost())
        logit("the final description is  ",mochWithIceCream.getDescription())

    },
    execute(dom) {
        dom.innerHTML = this.text
    }
})


let main = Main()
export default main
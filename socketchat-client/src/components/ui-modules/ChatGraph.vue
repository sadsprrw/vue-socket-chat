<template>
  <div class="graph">
    <h1 class="graph-header">Users Graph</h1>
    <svg :width="width" :height="height" class="graph-svg" id="graph"></svg>
  </div>
</template>

<script>
import 'd3-force'
import * as d3 from "d3";

export default {
  name: "ChatGraph",
  props: {
    userList: {
      require: true
    },
    connectionList: {
      require: true
    }
  },
  data() {
    return {
      nodes: [],
      links: [],
      simulation: null,
      link: null,
      node: null,
      width: window.innerWidth/2,
      height: 800,
      // simulationTime: 10000,
      startTime: 0
    }
  },
  mounted() {
    this.svg = d3.select('svg')
    this.svgDoc = document.getElementById('graph');
    console.log(this.svg.node().height)
    let width = this.svg.attr('width')
    let height = this.svg.attr('height')
    console.log(width, height)
    this.simulation = d3.forceSimulation(this.nodes)
        .force('charge', d3.forceManyBody().strength(-60))
        .force('link', d3.forceLink(this.links).distance(50))
        .force('x', d3.forceX())
        .force('y', d3.forceY())
        .alphaTarget(1)
        .on('tick', this.ticked)

    this.g = this.svg.append('g').attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')')
    this.link = this.g.append('g').attr('stroke', '#000').attr('stroke-width', 1.5).selectAll('.link')
    this.node = this.g.append('g').attr('stroke', '#fff').attr('stroke-width', 1.5).selectAll('.node')

    this.restart()

  },

  methods: {
    message: function(source , target){
      this.offset = this.svgDoc.getBoundingClientRect();
      let s_node = this.node.nodes().find(x => x.id === source.id),
          t_node = this.node.nodes().find(x => x.id === target.id)
      let s_abs_coords = this.getAbsoluteCoords(s_node),
          t_abs_coords = this.getAbsoluteCoords(t_node)
      // console.log("ALALALAL", s_node.style['fill'])
      let msg_circle = this.svg.append('circle')
          .attr('fill', s_node.style['fill'])
          .attr('class', 'message-circle')
          .attr('r', 5)
          .attr('cx', s_abs_coords.x)
          .attr('cy', s_abs_coords.y)
      msg_circle
          .transition()
          .duration(2000)
          .attr('cx', t_abs_coords.x)
          .attr('cy', t_abs_coords.y)
          .on('end', () =>{
            msg_circle.remove()
          })
    },
    getAbsoluteCoords(elem){
      let bbox = elem.getBBox(),
              middleX = bbox.x + (bbox.width / 2),
              middleY = bbox.y + (bbox.height / 2);
      let matrix = elem.getScreenCTM()
      return {
        x: (matrix.a * middleX) + (matrix.c * middleY) + matrix.e - this.offset.left,
        y: (matrix.b * middleX) + (matrix.d * middleY) + matrix.f - this.offset.top
      };
    },
    restart () {
      // let color = d3.scaleOrdinal(d3.schemeCategory10)
      this.startTime = Date.now()
      // Apply the general update pattern to the nodes
      this.node = this.node.data(this.nodes, function (d) { return d.id })
      this.node.exit().remove()
      this.node = this.node.enter().append('circle').attr('class', 'node').attr('style', function (d) { return "fill:"+d.color })
          .attr('id', function (d) { return d.id }).attr('r', 15).merge(this.node)
      // // Apply the general update pattern to the links

      this.link = this.link.data(this.links, function (d) {
        return d.source.id + '-' + d.target.id
      })

      this.link.exit().remove()
      this.link = this.link.enter().append('line').attr('class','link').merge(this.link)

      // Update and restart the simulation
      this.simulation.nodes(this.nodes)
      this.simulation.force('link').links(this.links)
      this.simulation.alpha(0).restart()

    },
    ticked () {
      // if (Date.now() < this.startTime + this.simulationTime){
        this.node.attr('cx', function (d) { return d.x })
            .attr('cy', function (d) { return d.y })
        this.link.attr('x1', function (d) { return d.source.x })
            .attr('y1', function (d) { return d.source.y })
            .attr('x2', function (d) { return d.target.x })
            .attr('y2', function (d) { return d.target.y })
      // }
      // else this.simulation.stop()
    },

    updateNodesData(users){
      let values = Object.values(users)
      this.nodes = this.nodes.filter(function (value){
        if (values.find(x => x['username'] === value['id']))
            return value;
      })
      values.forEach(user => {
        if (!this.nodes.find(x => x.id === user['username']))
          this.nodes.push({ id: user['username'], color: user['color']});
      })
      // for (const user in users){
      //   console.log("USER")
      //   console.log(user)
      //
      // }
      console.log("NODES")
      console.log(this.nodes)
      this.restart()
    },

    updateLinksData(links){
      console.log("Linker")

      this.links = this.links.filter(value => links.includes(value))
      console.log(this.links)
      console.log(links)
      links.forEach(link => {
        if (!this.links.find(x => (x['source'] === link['target'] && x['target'] === link['source']) ||
                                  (x['source'] === link['source'] && x['target'] === link['target']))) {
          let node1 = this.nodes.find(x => x.id === link['source']['id'])
          let node2 = this.nodes.find(x => x.id === link['target']['id'])
          this.links.push({source: node1, target: node2});
        }
      })
      console.log("Links")
      console.log(this.links)
      this.restart()
    }
  },

  watch: {
    userList: {
      handler(newUList) {
        console.log("NEW user LIST")
        console.log(newUList)
        this.updateNodesData(newUList);
      },
      deep: true
    },
    connectionList: {
      handler(newCList) {
        console.log("NEW Conn LIST")
        console.log(newCList)
        this.updateLinksData(newCList);
      },
      deep: true
    }
  }
}

</script>

<style scoped>
@import "../../scss/graph.css";
</style>
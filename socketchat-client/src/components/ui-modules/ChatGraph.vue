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

    const width = this.svg.attr('width')
    const height = this.svg.attr('height')

    this.simulation = d3.forceSimulation(this.nodes)
        .force('charge', d3.forceManyBody().strength(-300))
        .force('link', d3.forceLink(this.links).distance(100))
        .force('x', d3.forceX().x(width/2))
        .force('y', d3.forceY().y(height/2))
        .alphaTarget(1)
        .on('tick', this.ticked)

    this.g = this.svg.append('g').attr('id', 'everything')

    this.link = this.g.append('g').attr('stroke', '#000').attr('stroke-width', 1.5).selectAll('.link')
    this.node = this.g.append('g').attr('stroke', '#fff').attr('stroke-width', 1.5).selectAll('.node')


    this.svg.call(d3.zoom()
        .extent([[0, 0], [width, height]])
        .scaleExtent([1, 8])
        .on("zoom", this.zoomed));

    // this.node.call(drag).on("click", this.click);

    this.restart()
  },

  methods: {
    message: function(source , target){
      const s_node = this.node.nodes().find(x => x.id === source.id),
          t_node = this.node.nodes().find(x => x.id === target.id)

      const msg_circle = this.g.append('circle')
          .attr('fill', s_node.style['fill'])
          .attr('class', 'message-circle')
          .attr('r', 5)
          .attr('cx', s_node.getAttribute('cx'))
          .attr('cy', s_node.getAttribute('cy'))

      msg_circle
          .transition()
          .duration(2000)
          .attr('cx', t_node.getAttribute('cx'))
          .attr('cy', t_node.getAttribute('cy'))
          .on('end', () =>{
            msg_circle.remove()
          })
    },
    restart () {
      this.startTime = Date.now()

      this.node = this.node.data(this.nodes, function (d) { return d.id })
      this.node.exit().remove()
      this.node = this.node.enter()
          .append('circle')
          .attr('class', 'node')
          .attr('style', function (d) { return "fill:"+d.color })
          .attr('id', function (d) { return d.id })
          .attr('r', 15)
          .call(this.drag())
          .merge(this.node)

      this.link = this.link.data(this.links, function (d) {
        return d.source.id + '-' + d.target.id
      })

      this.link.exit().remove()
      this.link = this.link.enter().append('line').attr('class','link').merge(this.link)

      this.simulation.nodes(this.nodes)
      this.simulation.force('link').links(this.links)
      this.simulation.alpha(0).restart()

    },
    ticked () {
        this.node.attr('cx', function (d) { return d.x })
            .attr('cy', function (d) { return d.y })
        this.link.attr('x1', function (d) { return d.source.x })
            .attr('y1', function (d) { return d.source.y })
            .attr('x2', function (d) { return d.target.x })
            .attr('y2', function (d) { return d.target.y })
    },
    zoomed({transform}){
      this.g.attr("transform", transform);
    },
    drag(){
      const dragstarted = d => {

        d.fx = d.x;
        d.fy = d.y;
      };
      const dragged = (event, d) => {
        console.log(event)
        d.fx = event.x;
        d.fy = event.y;
      };
      const dragended = d => {

        d.fx = null;
        d.fy = null;
      };
      return d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended);
    },
    updateNodesData(users){
      const values = Object.values(users)
      this.nodes = this.nodes.filter(function (value){
        if (values.find(x => x['username'] === value['id']))
            return value;
      })
      values.forEach(user => {
        if (!this.nodes.find(x => x.id === user['username']))
          this.nodes.push({ id: user['username'], color: user['color']});
      })

      this.restart()
    },

    updateLinksData(links){
      this.links = this.links.filter(value => links.includes(value))

      links.forEach(link => {
        if (!this.links.find(x => (x['source'] === link['target'] && x['target'] === link['source']) ||
                                  (x['source'] === link['source'] && x['target'] === link['target']))) {
          const node1 = this.nodes.find(x => x.id === link['source']['id'])
          const node2 = this.nodes.find(x => x.id === link['target']['id'])
          this.links.push({source: node1, target: node2});
        }
      })

      this.restart()
    }
  },

  watch: {
    userList: {
      handler(newUList) {
        this.updateNodesData(newUList);
      },
      deep: true
    },
    connectionList: {
      handler(newCList) {
        this.updateLinksData(newCList);
      },
      deep: true
    }
  }
}

</script>

<style scoped>
@import "../../css/graph.css";
</style>
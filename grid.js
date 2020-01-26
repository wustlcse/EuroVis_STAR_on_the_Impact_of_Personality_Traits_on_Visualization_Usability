var table = d3.select("#table")
    .append("svg")
    .attr("width","1000px")
    .attr("height","2000px");
width = 12;
height= 12;
num_traits = 0;
num_vis = 0;
num_task = 0;
num_measures = 0;

color_dict = {
    'TRAITS': '#70ad47',
    'VIS': '#f4b183',
    'TASK': '#4472c4',
    'MEASURES': '#843c0c',
};

$.getJSON("cognitive_traits.json", function(json) {
    var reading = json;
    reading.sort(function(a, b) {
        return a['issued']['date-parts'][0][0] - b['issued']['date-parts'][0][0];
    });
    d3.json("paper_list.json", function(data) {
        console.log(data);
        reference_list = []; // store the paper names/references
        categories_list = []; // store the cell data for data()
        for(var i=0; i < data.length; ++i)
        {
            current = data[i];
            if(i==0)
            {
                num_traits = Object.keys(current['TRAITS']).length;
                num_vis= Object.keys(current['VIS']).length;
                num_task = Object.keys(current['TASK']).length;
                num_measures = Object.keys(current['MEASURES']).length;
                console.log(num_traits);
                console.log(num_vis);
                console.log(num_task);
                console.log(num_measures);

                traits_list = Object.keys(current['TRAITS']);
                vis_list = Object.keys(current['VIS']);
                task_list = Object.keys(current['TASK']);
                measures_list = Object.keys(current['MEASURES']);
            }
            reference_list.push(current['reference'].replace(/[\\']/g,""));
            categories_list.push([]);
            field_count = 0;
            for (var property in current)
            {
                if (current.hasOwnProperty(property))
                {
                    sub_current = current[property];
                    if(typeof sub_current === 'object')
                    {
                        for (var sub_property in sub_current)
                        {
                            if (sub_current.hasOwnProperty(sub_property))
                            {
                                categories_list[i].push(
                                    {
                                        paper_name: current['reference'],
                                        category_name: property,
                                        sub_property_name: sub_property,
                                        sub_property_value: sub_current[sub_property],
                                        y: i+1,
                                        x: field_count+1
                                    }
                                );
                                ++field_count;
                            }
                        }
                    }
                }
            }
        }
        console.log(categories_list);




        var row = table.selectAll(".row")
            .data(categories_list)
            .enter().append("g")
            .attr("class", "row")
            .attr("transform", "translate(120,100)")
        ;

        var column = row.selectAll(".cell")
            .data(function(d)
            {
                //console.log(d);
                return d;
            })
            .enter().append("rect")
            .attr("class","cell")
            .attr("x", function(d)
            {
                //console.log(d);
                if(d.category_name == 'VIS')
                {
                    return 20*d.x+1+30;
                }

                if(d.category_name == 'TASK')
                {
                    return 20*d.x+1+60;
                }

                if(d.category_name == 'MEASURES')
                {
                    return 20*d.x+90;
                }
                return 20*d.x+1;
            })
            .attr("y", function(d) { return 20*d.y+1; })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", function(d) { return width; })
            .attr("height", function(d) { return height; })
            .style("fill", function (d) {
                console.log(d.sub_property_value);
                var value = d.sub_property_value;

                if(value == 'noA')
                {
                    x_mark = 0;
                    y_mark = 0;
                    if(d.category_name == 'VIS')
                    {
                        x_mark = 20*d.x+1+30;
                    }
                    if(d.category_name == 'TASK')
                    {
                        x_mark = 20*d.x+1+60;
                    }
                    if(d.category_name == 'MEASURES')
                    {
                        x_mark =  20*d.x+90;
                    }
                    else {
                        x_mark = 20*d.x+1;
                    }
                    row.append("text")
                        .attr("x", x_mark+6)
                        .attr("y", 20*d.y+9).attr("text-anchor", "middle")
                        .style("font-size", "8px")
                        .style("fill",'white')
                        .text('X');
                    return color_dict[d.category_name];
                }
                if(value.search('yes')!=-1)
                {
                    return color_dict[d.category_name];
                }
                return "#e9e9e9";
            })
        ;

        var tooltip = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("z-index", "5")
            .style("visibility", "hidden")
            .style("background-color", "white")
            .style("border", "solid")
            .style("border-width", "1px")
            .style("border-radius", "5px")
            .style("display","block")
            .style("width","500px")
            .html("");

        for(var i = 0;i<reference_list.length;++i)
        {
            table.append("text")
                .attr("x", 130)
                .attr("y", 20*i+130+1)
                .attr("text-anchor", "end")
                .attr("class","ref")
                .style("font-size", "10px")
                .text(reference_list[i])
                .attr("id",function () {
                    if(i < 10)
                    {
                        return '0'+i.toString()+reference_list[i];
                    }
                    return i.toString()+reference_list[i];

                })
                .on("mouseover", function(e)
                {
                    return tooltip.style("visibility", "visible");
                })
                .on("mousemove", function(){return tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px");})
                .on("mouseout", function(){return tooltip.style("visibility", "hidden");});
        }

        $(document).on('mouseover','text', function(e) {
            target_class = $(e.target).attr('class');
            if(target_class == 'ref')
            {
                index = parseInt(e.target.id.substring(0,2));
                console.log("current index is " + index);
                reading_object = reading[index];
                title = reading_object['title']
                abstract = reading_object['abstract']
                tooltip.html(function () {
                    return "<p>" + title + "</p>"+"<p>" + abstract + "</p>";
                }) ;
            }
        });

        for(var i = 0;i<traits_list.length;++i)
        {
            table.append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("text-anchor", "start")
                .style("font-size", "10px")
                .text(traits_list[i])
                .attr("transform", function(d){
                    var xText = 150+i*20;
                    var yText = 110;
                    return "translate(" + xText + "," + yText + ") rotate(-90)";
                });
        }

        for(var i = 0;i<vis_list.length;++i)
        {
            table.append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("text-anchor", "start")
                .style("font-size", "10px")
                .text(vis_list[i])
                .attr("transform", function(d){
                    var xText = 150+i*20+30+traits_list.length*20;
                    var yText = 110;
                    return "translate(" + xText + "," + yText + ") rotate(-90)";
                });
        }

        for(var i = 0;i<task_list.length;++i)
        {
            table.append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("text-anchor", "start")
                .style("font-size", "10px")
                .text(task_list[i])
                .attr("transform", function(d){
                    var xText = 150+i*20+30*2+(traits_list.length+vis_list.length)*20;
                    var yText = 110;
                    return "translate(" + xText + "," + yText + ") rotate(-90)";
                });
        }

        for(var i = 0;i<measures_list.length;++i)
        {
            table.append("text")
                .attr("x", 0)
                .attr("y", 0)
                .attr("text-anchor", "start")
                .style("font-size", "10px")
                .text(function (d) {
                    current_measure = measures_list[i];
                    console.log(typeof  current_measure);
                    if(current_measure.search("Other Quantitative")!=-1)
                    {
                        return "Other Quantitative";
                    }
                    return current_measure;
                })
                .attr("transform", function(d){
                    var xText = 150+i*20+30*3+(traits_list.length+vis_list.length+task_list.length)*20;
                    var yText = 110;
                    return "translate(" + xText + "," + yText + ") rotate(-90)";
                });
        }

    });
});





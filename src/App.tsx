import React from "react";
import { useState, useEffect, useRef } from "react";
import { Button, Input } from "@nextui-org/react";
import axios from "axios";
import { Chart } from "chart.js";
import * as echarts from "echarts";
import { GraphData } from "./graphdata";

type EChartsOption = echarts.EChartsOption;

function App(): JSX.Element {
  // Values of the inputs
  const [functionX, setFunctionX] = useState<string>("");
  const [aValue, setAValue] = useState<number>(0);
  const [nValue, setNValue] = useState<number>(0);
  const [xValue, setXValue] = useState<number>(0);

  // Graph element
  const graphElement = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const params = {
      f_entry: functionX,
      a_entry: aValue,
      n_entry: nValue,
      x_entry: xValue,
    };

    axios.get("http://localhost:8000/taylor", { params }).then((response) => {
      const error = response.data["error"];

      if (!error) {
        const data: GraphData = response.data["data"];

        let myChart = echarts.init(graphElement.current);
        let option: EChartsOption;

        option = {
          xAxis: {
            type: "value",
          },
          yAxis: {
            type: "value",
          },
          series: [
            {
              data: [820, 932, 901, 934, 1290, 1330, 1320],
              type: "line",
              smooth: true,
            },
          ],
        };

        myChart.setOption(option);
      }
    });
  }, [functionX, aValue, nValue, xValue]);

  return (
    <div className="flex flex-col gap-4 justify-center items-center h-screen">
      <div>
        <h1 className="text-8xl font-bold text-gray-300">SERIES DE TAYLOR</h1>
      </div>
      <div className="flex gap-3">
        <Input
          size="md"
          type="text"
          label="Function f(x)"
          onValueChange={(e) => {
            setFunctionX(e);
          }}
        />
        <Input
          size="md"
          type="number"
          label="A value"
          onValueChange={(e) => {
            setAValue(Number(e));
          }}
        />
        <Input
          size="md"
          type="number"
          label="N value"
          onValueChange={(e) => {
            setNValue(Number(e));
          }}
        />
        <Input
          size="md"
          type="number"
          label="X value"
          onValueChange={(e) => {
            setXValue(Number(e));
          }}
        />
      </div>
      <div>
        <div ref={graphElement} width={600} height={400}></div>
      </div>
    </div>
  );
}

export default App;

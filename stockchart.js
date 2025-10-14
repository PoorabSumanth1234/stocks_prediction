// components/StockChart.js
"use client";

import React from 'react';
import dynamic from 'next/dynamic';
const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

const StockChart = ({ chartData, ticker }) => {
  const options = {
    chart: {
      type: 'candlestick', // Change chart type
      height: 350,
      animations: { enabled: false },
      toolbar: { show: false },
      zoom: { enabled: true }
    },
    title: {
      text: `${ticker.toUpperCase()} Stock Price`,
      align: 'left',
      style: { color: '#FFFFFF' }
    },
    xaxis: {
      type: 'datetime',
      labels: { style: { colors: '#9CA3AF' } }
    },
    yaxis: {
      tooltip: { enabled: true },
      labels: {
        formatter: (value) => `$${value.toFixed(2)}`,
        style: { colors: '#9CA3AF' }
      }
    },
    grid: { borderColor: '#4B5563' },
    tooltip: { theme: 'dark' },
    theme: { mode: 'dark' }
  };

  const series = [{
    // The component now expects the data in this new format
    data: chartData 
  }];
  
  if (typeof window === 'undefined') {
    return <div>Loading Chart...</div>;
  }

  return (
    <div className="chart-container w-full p-4 bg-gray-800 rounded-lg shadow-md">
      <Chart options={options} series={series} type="candlestick" height={350} />
    </div>
  );
};

export default StockChart;
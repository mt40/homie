$.get(line_chart_json_url, function (data) {
  for(let i = 1; i <= 3; i++) {
    const ctx = $(`#myChart${i}`).get(0).getContext("2d");
    new Chart(ctx, {
      type: 'line',
      data: data,
      options: {
        showLines: true,
        scales: {
          yAxes: [{
            gridLines: {
              display: false,
            },
            // display: false,
          }],
          xAxes: [{
            gridLines: {
              display: false,
            },
          }],
        },
      }
    });
  }
});
const updateattribute = (value) =>
{
    document.getElementById("value").textContent = value;
};


new QWebChannel(qt.webChannelTransport,
   (channel) => {
   var server = channel.objects.server;
   window.server = server;
   server.value_changed.connect(updateattribute);
   server.factorial_changed.connect((value) => {
    document.getElementById("value2").textContent = value;
   });
   alert("Channel setted");
  });

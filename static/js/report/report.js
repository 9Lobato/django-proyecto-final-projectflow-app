// static\js\report\report.js ...
// ... se utiliza en:
// templates\report\report.html en la visualización de los gráficos e informes


// =========================================
// GRÁFICOS DEL INFORME
// Inicializa los gráficos de proyectos, tareas,
// carga de trabajo, productividad y participación.
// =========================================

// Métrica proyectos creados
const projectsCanvas = document.getElementById("projectsChart");
if (projectsCanvas) {
  new Chart(projectsCanvas, {
    type: "bar",
    data: {
      labels: reportData.months,
      datasets: [{
        label: "Proyectos",
        data: reportData.projects_month,
        borderWidth: 1,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          displayColors: false,
          callbacks: {
            title: function() {
              return "";
            },
            label: function(context) {
              const index = context.dataIndex;
              const codes = reportData.projects_created_codes[index] || [];
              return codes.length
                ? codes
                : "Sin proyectos";
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 5,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
}

// Métrica proyectos archivados
const archivedCanvas = document.getElementById("projectsArchivedChart");
if (archivedCanvas) {
  new Chart(archivedCanvas, {
    type: "bar",
    data: {
      labels: reportData.archived_months,
      datasets: [{
        label: "Archivados",
        data: reportData.projects_archived_month,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          displayColors: false,
          callbacks: {
            title: function() {
              return "";
            },
            label: function(context) {
              const index = context.dataIndex;
              const codes = reportData.projects_archived_codes[index] || [];
              return codes.length
                ? codes
                : "Sin proyectos";
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 5,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
}

// Evolución del progreso de proyectos
const progressCanvas = document.getElementById("projectsCompletedChart");
if (progressCanvas) {
  const progressTitle = progressCanvas
    .closest(".card")
    .querySelector(".card-header h4");
  const progressChart =
    new Chart(progressCanvas, {
      type: "line",
      data: {
        labels: reportData.progress_labels,
        datasets: reportData.progress_datasets.map(
          (dataset, index) => {
            const activeColors = ["#4e79a7", "#59a14f", "#f28e2b", "#e15759", "#b07aa1", "#76b7b2", "#edc949", "#af7aa1"];
            const activeDatasetIndex =
              reportData.progress_datasets
                .slice(0, index)
                .filter(item => !item.archived)
                .length;
            const color = dataset.archived
              ? "#dee2e6"
              : activeColors[activeDatasetIndex % activeColors.length];
            return {
              label: dataset.label,
              data: dataset.data,
              tension: 0.3,
              fill: false,
              pointRadius: 0,
              pointHoverRadius: 4,
              pointHitRadius: 10,
              archived: dataset.archived,
              interpolated: dataset.interpolated,
              archiveIndex: dataset.archive_index,
              borderColor: color,
              backgroundColor: color,
              borderWidth: 2,
            };
          }
        ),
      },
      options: {
        responsive: true,
        interaction: {mode: "nearest", intersect: false},
        onHover:
          function(event, elements) {
            if (elements.length) {
              const datasetIndex = elements[0].datasetIndex;
              const dataset = progressChart.data.datasets[datasetIndex];
              // Los proyectos archivados no se pueden aislar.
              if (dataset.archived) {event.native.target.style.cursor = "default";
                return;
              }
              event.native.target.style.cursor = "pointer";
            } else {
              event.native.target.style.cursor = "default";
            }
          },
        onClick:
          function(event, elements) {
            if (!elements.length) {
              return;
            }
            const clickedDatasetIndex = elements[0].datasetIndex;
            const datasets = progressChart.data.datasets;
            const clickedDataset = datasets[clickedDatasetIndex];
            // Un proyecto archivado no puede aislarse.
            if (clickedDataset.archived) {
              return;
            }
            const onlyVisible = datasets.filter(dataset => !dataset.hidden);
            const isFiltered = onlyVisible.length === 1 && !clickedDataset.hidden;
            // Restaurar todos
            if (isFiltered) {
              datasets.forEach(
                dataset => {
                  dataset.hidden = false;
                }
              );
              progressTitle.textContent = "Progreso proyectos";
              progressChart.update();
              return;
            }
            // Aislar proyecto activo
            datasets.forEach(
              (dataset, index) => {dataset.hidden = index !== clickedDatasetIndex}
            );
            progressTitle.textContent = "Progreso " + clickedDataset.label;
            progressChart.update();
          },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback:
                function(value) {return value + "%"}
            }
          }
        },
        plugins: {
          legend: {display: false},
          tooltip: {
            callbacks: {
              title:
                function(context) {
                  return context[0]
                    .dataset
                    .label;
                },
              label:
                function(context) {
                  const dataset = context.dataset;
                  const index = context.dataIndex;
                  const value = context.raw;
                  if (
                    value === null ||
                    value === undefined
                  ) {
                    return "";
                  }
                  const isInterpolated = dataset.interpolated && dataset.interpolated[index];
                  return (
                    value +
                    "%" +
                    (
                      isInterpolated
                        ? "*"
                        : ""
                    )
                  );
                }
            }
          }
        }
      }
    });
}

// Donut de estado
const ctx = document.getElementById("taskStatusChart");
if (ctx) {
  const statusMap = {
    "To do": "TODO",
    "In progress": "IN_PROGRESS",
    "Done": "DONE",
    "Cancelled": "CANCELLED",
  };
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: reportData.status_labels,
      datasets: [{
        data: reportData.status_data,
        backgroundColor: [
          "#9AD0F5",
          "#B8E0D2",
          "#F7D6A3",
          "#D8B4E2"
        ],
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      onHover(event, elements) {
        event.native.target.style.cursor =
          elements.length ? "pointer" : "default";
      },
      onClick(event, elements) {
        if (!elements.length) return;
        const index = elements[0].index;
        const label = this.data.labels[index];
        const status = statusMap[label];
        window.location.href =
          `${TASK_LIST_URL}?created_by=&assigned_to=&status=${status}` +
          `&delivery=NO_LIMIT&delivery=ON_TIME&delivery=OVERDUE` +
          `&priority_all=&search=`;
      },
      plugins: {
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            padding: 18
          }
        },
        tooltip: {
          callbacks: {
            label(context) {
              const value = context.raw;
              const total = context.dataset.data.reduce(
                (a, b) => a + b,
                0
              );
              const percentage = total
                ? Math.round(value / total * 100)
                : 0;
              return `${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

// Donut de entrega
const deliveryCanvas = document.getElementById("taskDeliveryChart");
if (deliveryCanvas) {
  const deliveryMap = {
    "Sin límite": "NO_LIMIT",
    "Archivadas": "ARCHIVED",
    "Vencidas": "OVERDUE",
    "En plazo": "ON_TIME",
  };
  new Chart(deliveryCanvas, {
    type: "doughnut",
    data: {
      labels: reportData.delivery_labels,
      datasets: [{
        data: reportData.delivery_data,
        backgroundColor: [
          "#9AD0F5",
          "#B8E0D2",
          "#F7D6A3",
          "#D8B4E2"
        ],
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      onHover(event, elements) {
        event.native.target.style.cursor =
          elements.length ? "pointer" : "default";
      },
      onClick(event, elements) {
        if (!elements.length) return;
        const index = elements[0].index;
        const label = this.data.labels[index];
        const delivery = deliveryMap[label];
        window.location.href =
          `${TASK_LIST_URL}?created_by=&assigned_to=&status_all=` +
          `&delivery=${delivery}` +
          `&priority_all=&search=`;
      },
      plugins: {
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            padding: 18
          }
        },
        tooltip: {
          callbacks: {
            label(context) {
              const value = context.raw;
              const data = context.dataset.data;
              const total = data.reduce(
                (sum, item) => sum + item,
                0
              );
              const percentage = total
                ? Math.round((value / total) * 100)
                : 0;
              return `${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

// Donut de prioridad
const priorityCanvas = document.getElementById("taskPriorityChart");
if (priorityCanvas) {
  const priorityMap = {
    "Baja": "LOW",
    "Media": "MEDIUM",
    "Alta": "HIGH",
  };
  new Chart(priorityCanvas, {
    type: "doughnut",
    data: {
      labels: reportData.priority_labels,
      datasets: [{
        data: reportData.priority_data,
        backgroundColor: [
          "#9AD0F5",
          "#B8E0D2",
          "#F7D6A3",
          "#D8B4E2"
        ],
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      onHover(event, elements) {
        event.native.target.style.cursor =
          elements.length ? "pointer" : "default";
      },
      onClick(event, elements) {
        if (!elements.length) return;
        const index = elements[0].index;
        const label = this.data.labels[index];
        const priority = priorityMap[label];
        window.location.href =
          `${TASK_LIST_URL}?created_by=&assigned_to=&status_all=` +
          `&delivery=NO_LIMIT&delivery=ON_TIME&delivery=OVERDUE` +
          `&priority=${priority}&search=`;
      },
      plugins: {
        legend: {
          position: "bottom",
          align: "center",
          labels: {
            boxWidth: 20,
            padding: 18
          }
        },
        tooltip: {
          callbacks: {
            label(context) {
              const value = context.raw;
              const data = context.dataset.data;
              const total = data.reduce(
                (sum, item) => sum + item,
                0
              );
              const percentage = total
                ? Math.round((value / total) * 100)
                : 0;

              return `${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}

// Carga de trabajo
const workloadCanvas = document.getElementById("userLoadChart");
if (workloadCanvas) {
  new Chart(workloadCanvas, {
    type: "bar",
    data: {
      labels: reportData.user_labels,
      datasets: [{
        label: "Tareas activas",
        data: reportData.user_tasks,
        borderRadius: 6
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
}

// Productividad
const productivityCanvas = document.getElementById("productivityChart");
if (productivityCanvas) {
  new Chart(productivityCanvas, {
    type: "bar",
    data: {
      labels: reportData.productivity_labels,
      datasets: [{
        label: "Productividad (%)",
        data: reportData.productivity_data
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: function(context) {
              return context[0].label;
            },
            label: function(context) {
              return "Productividad: " + context.raw + "%";
            }
          }
        }
      },
      scales: {
        x: {
          beginAtZero: true,
          min: 0,
          max: 100,
          ticks: {
            stepSize: 10,
            callback: function(value) {
              return value + "%";
            }
          }
        }
      }
    }
  });
}

// Participación
const participationCanvas =
  document.getElementById("participationChart");
if (participationCanvas) {
  new Chart(participationCanvas, {
    type: "bar",
    data: {
      labels: reportData.participation_labels,
      datasets: [{
        label: "Participación (%)",
        data: reportData.participation_data
      }]
    },
    options: {
      indexAxis: "y",
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          beginAtZero: true,
          min: 0,
          max: 100,
          ticks: {
            callback: value => value + "%"
          }
        }
      }
    }
  });
}

// Popover
document.querySelectorAll('[data-bs-toggle="popover"]').forEach(element => {
  new bootstrap.Popover(element);
});

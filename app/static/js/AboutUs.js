import React from 'react';
import * as Lucide from 'lucide-react';

const Presentation = () => {
  const [currentSlide, setCurrentSlide] = React.useState(0);
  const [isFullscreen, setIsFullscreen] = React.useState(false);

  const createIcon = (IconComponent) => React.createElement(IconComponent, {
    size: 48,
    style: { color: '#3b82f6' }
  });

  const createListItem = (text, key) => React.createElement("p", {
    key,
    style: {
      fontSize: '1.125rem',
      color: '#4b5563',
      display: 'flex',
      alignItems: 'flex-start',
      gap: '4px',
      marginBottom: '0px',
      lineHeight: '1.2'
    }
  }, [
    React.createElement("span", {
      key: "bullet",
      style: { color: '#3b82f6', lineHeight: '1.2' }
    }, "•"),
    React.createElement("span", {
      key: "text",
      style: { lineHeight: '1.2' }
    }, text)
  ]);

  const slides = [
    {
      title: "DroMo",
      icon: createIcon(Lucide.Box),
      content: React.createElement("div", {
        style: {
          textAlign: 'center',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px'
        }
      }, [
        React.createElement("h2", {
          key: "title",
          style: {
            fontSize: '2.25rem',
            fontWeight: 'bold',
            background: 'linear-gradient(to right, #3b82f6, #8b5cf6)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }
        }, "DroMo: Automated 3D Reconstruction System"),
        React.createElement("p", {
          key: "subtitle",
          style: { fontSize: '1.25rem', color: '#4b5563' }
        }, "Transform Reality into Digital 3D"),
        React.createElement("div", {
          key: "credits",
          style: { marginTop: '32px', color: '#374151' }
        }, [
          React.createElement("p", { key: "authors" }, "By: Dor Ferenc & Alon Shlomi"),
          React.createElement("p", { key: "advisor" }, "Advisor: Michael Gorelik")
        ])
      ])
    },
    {
      title: "What is DroMo?",
      icon: createIcon(Lucide.Info),
      content: React.createElement("div", {
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "features",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '12px'
            }
          }, "Key Features"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Automated point cloud processing", "feat1"),
            createListItem("Advanced mesh generation", "feat2"),
            createListItem("Texture mapping and UV coordination", "feat3"),
            createListItem("RESTful API integration", "feat4"),
            createListItem("User-friendly web interface", "feat5"),
            createListItem("Industry-standard OBJ output format", "feat6")
          ])
        ]),
        React.createElement("div", {
          key: "explanation",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "DroMo Explained"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            React.createElement("p", {
              style: {
                fontSize: '1.125rem',
                color: '#4b5563',
                lineHeight: '1.5'
              }
            }, "DroMo is an automated 3D reconstruction system designed to transform LIDAR point cloud data into high-quality 3D models. It streamlines the entire process from scan to finished model, making professional-grade 3D reconstruction accessible and efficient."),
            React.createElement("p", {
              style: {
                fontSize: '1.125rem',
                color: '#4b5563',
                lineHeight: '1.5'
              }
            }, "The system handles everything from initial data processing to final model generation, requiring minimal user intervention while maintaining high quality standards.")
          ])
        ])
      ])
    },
    {
      title: "System Architecture",
      icon: createIcon(Lucide.Layers),
      content: React.createElement("div", {
        style: {
          display: 'flex',
          flexDirection: 'column',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "architecture-diagram",
          style: {
            padding: '20px',
            backgroundColor: '#f8fafc',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1f2937',
              marginBottom: '16px',
              textAlign: 'center'
            }
          }, "Core Components"),
          React.createElement("div", {
            style: {
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '16px'
            }
          }, [
            ["User Interface", "Web-based interface, API access"],
            ["Services Layer", "PreprocessService, ReconstructionService, VisualsService"],
            ["Data Layer", "MongoDB, File Storage"]
          ].map(([title, desc], idx) =>
            React.createElement("div", {
              key: `component-${idx}`,
              style: {
                padding: '16px',
                backgroundColor: 'white',
                borderRadius: '8px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                textAlign: 'center'
              }
            }, [
              React.createElement("h4", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#3b82f6',
                  marginBottom: '8px'
                }
              }, title),
              React.createElement("p", {
                style: {
                  color: '#4b5563'
                }
              }, desc)
            ]))
          )
        ]),
        React.createElement("div", {
          key: "data-flow",
          style: {
            padding: '20px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1f2937',
              marginBottom: '16px',
              textAlign: 'center'
            }
          }, "Data Flow"),
          React.createElement("div", {
            style: {
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '0 32px'
            }
          }, [
            React.createElement("div", {
              style: {
                textAlign: 'center'
              }
            }, [
              React.createElement(Lucide.Upload, {
                size: 32,
                color: '#3b82f6'
              }),
              React.createElement("p", {
                style: {
                  marginTop: '8px',
                  color: '#4b5563'
                }
              }, "Input")
            ]),
            React.createElement(Lucide.ArrowRight, {
              size: 24,
              color: '#9ca3af'
            }),
            React.createElement("div", {
              style: {
                textAlign: 'center'
              }
            }, [
              React.createElement(Lucide.Cog, {
                size: 32,
                color: '#3b82f6'
              }),
              React.createElement("p", {
                style: {
                  marginTop: '8px',
                  color: '#4b5563'
                }
              }, "Processing")
            ]),
            React.createElement(Lucide.ArrowRight, {
              size: 24,
              color: '#9ca3af'
            }),
            React.createElement("div", {
              style: {
                textAlign: 'center'
              }
            }, [
              React.createElement(Lucide.Box, {
                size: 32,
                color: '#3b82f6'
              }),
              React.createElement("p", {
                style: {
                  marginTop: '8px',
                  color: '#4b5563'
                }
              }, "Output")
            ])
          ])
        ])
      ])
    },
    {
      title: "Technical Stack",
      icon: createIcon(Lucide.Code),
      content: React.createElement("div", {
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "core-tech",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '12px'
            }
          }, "Core Technologies"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Backend: Python, Flask", "tech1"),
            createListItem("Database: MongoDB", "tech2"),
            createListItem("Containerization: Docker", "tech3"),
            createListItem("Version Control: Git", "tech4")
          ])
        ]),
        React.createElement("div", {
          key: "libraries",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "Core Libraries"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Open3D (Point cloud processing)", "lib1"),
            createListItem("NumPy/SciPy (Numerical operations)", "lib2"),
            createListItem("PyVista (3D visualization)", "lib3"),
            createListItem("Flask-RESTful (API framework)", "lib4")
          ])
        ])
      ])
    },
    {
        title: "Processing Pipeline",
        icon: createIcon(Lucide.GitBranch),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '16px'
          }
        }, [
          React.createElement("div", {
            style: {
              padding: '20px',
              backgroundColor: '#f8fafc',
              borderRadius: '12px',
              textAlign: 'center'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                color: '#1f2937',
                marginBottom: '20px'
              }
            }, "Pipeline Overview"),
            React.createElement("div", {
              style: {
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '0 32px'
              }
            },
              [
                {
                  title: "Input",
                  desc: "LIDAR scan (.ply format)"
                },
                {
                  title: "Preprocessing",
                  desc: "Point cloud optimization"
                },
                {
                  title: "Reconstruction",
                  desc: "Mesh generation"
                },
                {
                  title: "Output",
                  desc: "OBJ model with textures"
                }
              ].map((item, idx, arr) => (
                React.createElement(React.Fragment, { key: `stage-group-${idx}` }, [
                  React.createElement("div", {
                    style: {
                      textAlign: 'center'
                    }
                  }, [
                    React.createElement("div", {
                      style: {
                        width: '64px',
                        height: '64px',
                        borderRadius: '50%',
                        backgroundColor: '#3b82f6',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto',
                        marginBottom: '8px'
                      }
                    },
                      React.createElement("span", {
                        style: {
                          color: 'white',
                          fontSize: '1.5rem',
                          fontWeight: 'bold'
                        }
                      }, idx + 1)
                    ),
                    React.createElement("h4", {
                      style: {
                        fontSize: '1.125rem',
                        fontWeight: 'bold',
                        color: '#1f2937',
                        marginBottom: '4px'
                      }
                    }, item.title),
                    React.createElement("p", {
                      style: {
                        color: '#4b5563',
                        fontSize: '0.875rem'
                      }
                    }, item.desc)
                  ]),
                  idx < arr.length - 1 &&
                    React.createElement(Lucide.ArrowRight, {
                      key: `arrow-${idx}`,
                      size: 24,
                      color: '#9ca3af'
                    })
                ])
              ))
            )
          ])
        ])
      },
    {
      title: "Processing Pipeline - Preprocessing",
      icon: createIcon(Lucide.Filter),
      content: React.createElement("div", {
        style: {
          display: 'flex',
          flexDirection: 'column',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          style: {
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '16px'
          }
        }, [
          React.createElement("div", {
            key: "steps",
            style: {
              padding: '16px',
              backgroundColor: '#eff6ff',
              borderRadius: '12px'
            }
        }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                color: '#1d4ed8',
                marginBottom: '12px'
            }
          }, "Preprocessing Steps"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("1. Statistical outlier removal", "step1"),
            createListItem("2. Voxel-based downsampling", "step2"),
            createListItem("3. Normal vector estimation", "step3"),
            createListItem("4. Background plane removal (RANSAC)", "step4"),
            createListItem("5. Object clustering (DBSCAN)", "step5"),
            createListItem("6. Bottom surface reconstruction", "step6"),
            createListItem("7. Final point cloud optimization", "step7")
          ])
        ]),
        React.createElement("div", {
          key: "benefits",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "Benefits"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Improved data quality", "benefit1"),
            createListItem("Reduced noise and artifacts", "benefit2"),
            createListItem("Better surface reconstruction", "benefit3"),
            createListItem("Optimized processing time", "benefit4"),
            createListItem("Enhanced final model accuracy", "benefit5")
          ])
        ])
      ])
    ])
  },
  {
    title: "Processing Pipeline - Reconstruction",
    icon: createIcon(Lucide.Boxes),
    content: React.createElement("div", {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(2, 1fr)',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        key: "reconstruction-steps",
        style: {
          padding: '16px',
          backgroundColor: '#eff6ff',
          borderRadius: '12px'
        }
      }, [
        React.createElement("h3", {
          style: {
            fontSize: '1.25rem',
            fontWeight: 'bold',
            color: '#1d4ed8',
            marginBottom: '12px'
          }
        }, "Reconstruction Process"),
        React.createElement("div", {
          style: { display: 'flex', flexDirection: 'column', gap: '8px' }
        }, [
          createListItem("1. Alpha value optimization", "rec1"),
          createListItem("2. Delaunay triangulation", "rec2"),
          createListItem("3. Sealed surface mesh extraction", "rec3"),
          createListItem("4. Mesh cleaning and optimization", "rec4"),
          createListItem("5. UV mapping", "rec5"),
          createListItem("6. Texture application", "rec6"),
          createListItem("7. Final model generation", "rec7")
        ])
      ]),
      React.createElement("div", {
        key: "output",
        style: {
          padding: '16px',
          backgroundColor: '#f0fdf4',
          borderRadius: '12px'
        }
      }, [
        React.createElement("h3", {
          style: {
            fontSize: '1.25rem',
            fontWeight: 'bold',
            color: '#15803d',
            marginBottom: '12px'
          }
        }, "Output Specifications"),
        React.createElement("div", {
          style: { display: 'flex', flexDirection: 'column', gap: '8px' }
        }, [
          createListItem("Industry-standard OBJ format", "out1"),
          createListItem("High-quality texture maps", "out2"),
          createListItem("Optimized mesh topology", "out3"),
          createListItem("Proper UV unwrapping", "out4"),
          createListItem("Ready for 3D applications", "out5")
        ])
      ])
    ])
  },
  {
    title: "System Demo",
    icon: createIcon(Lucide.Monitor),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        key: "demo-stages",
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "input-stage",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '12px'
            }
          }, "Input Stage"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("LIDAR scan upload", "in1"),
            createListItem("Format validation", "in2"),
            createListItem("Initial visualization", "in3")
          ])
        ]),
        React.createElement("div", {
          key: "processing-stage",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "Processing Stage"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Progress tracking", "proc1"),
            createListItem("Real-time updates", "proc2"),
            createListItem("Status indicators", "proc3")
          ])
        ]),
        React.createElement("div", {
          key: "output-stage",
          style: {
            padding: '16px',
            backgroundColor: '#f0fdf4',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#15803d',
              marginBottom: '12px'
            }
          }, "Output Stage"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("3D model preview", "out1"),
            createListItem("Export options", "out2"),
            createListItem("Quality validation", "out3")
          ])
        ])
      ])
    ])
  },
  {
    title: "Test Results",
    icon: createIcon(Lucide.BarChart),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        key: "performance-metrics",
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "small-files",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px',
            textAlign: 'center'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '8px'
            }
          }, "Small Files"),
          React.createElement("p", {
            style: {
              fontSize: '1rem',
              color: '#4b5563',
              marginBottom: '8px'
            }
          }, "200k-400k points"),
          React.createElement("div", {
            style: {
              fontSize: '1.5rem',
              fontWeight: 'bold',
              color: '#1d4ed8'
            }
          }, [
            React.createElement("p", null, "4s"),
            React.createElement("p", null, "95% success")
          ])
        ]),
        React.createElement("div", {
          key: "medium-files",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px',
            textAlign: 'center'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '8px'
            }
          }, "Medium Files"),
          React.createElement("p", {
            style: {
              fontSize: '1rem',
              color: '#4b5563',
              marginBottom: '8px'
            }
          }, "400k-1M points"),
          React.createElement("div", {
            style: {
              fontSize: '1.5rem',
              fontWeight: 'bold',
              color: '#7e22ce'
            }
          }, [
            React.createElement("p", null, "14s"),
            React.createElement("p", null, "90% success")
          ])
        ]),
        React.createElement("div", {
          key: "large-files",
          style: {
            padding: '16px',
            backgroundColor: '#f0fdf4',
            borderRadius: '12px',
            textAlign: 'center'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#15803d',
              marginBottom: '8px'
            }
          }, "Large Files"),
          React.createElement("p", {
            style: {
              fontSize: '1rem',
              color: '#4b5563',
              marginBottom: '8px'
            }
          }, "1M-3M points"),
          React.createElement("div", {
            style: {
              fontSize: '1.5rem',
              fontWeight: 'bold',
              color: '#15803d'
            }
          }, [
            React.createElement("p", null, "25s"),
            React.createElement("p", null, "86% success")
          ])
        ])
      ])
    ])
  },
  {
    title: "Key Achievements",
    icon: createIcon(Lucide.Trophy),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        key: "achievements-grid",
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "technical-achievements",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '12px'
            }
          }, "Technical Achievements"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Successful automated 3D reconstruction pipeline", "tech1"),
            createListItem("Robust preprocessing algorithms", "tech2"),
            createListItem("Efficient point cloud to mesh conversion", "tech3"),
            createListItem("High-quality texture mapping", "tech4")
          ])
        ]),
        React.createElement("div", {
          key: "system-achievements",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "System Achievements"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("User-friendly API system", "sys1"),
            createListItem("Industry-standard output formats", "sys2"),
            createListItem("Scalable architecture", "sys3"),
            createListItem("Modular system design", "sys4")
          ])
        ])
      ])
    ])
  },
  {
    title: "Challenges & Solutions",
    icon: createIcon(Lucide.Lightbulb),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "challenges",
          style: {
            padding: '16px',
            backgroundColor: '#fee2e2',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#dc2626',
              marginBottom: '12px'
            }
          }, "Challenges"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Limited domain knowledge", "ch1"),
            createListItem("Consumer-grade LIDAR limitations", "ch2"),
            createListItem("War situation impact", "ch3"),
            createListItem("Complex geometry handling", "ch4")
          ])
        ]),
        React.createElement("div", {
          key: "solutions",
          style: {
            padding: '16px',
            backgroundColor: '#f0fdf4',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#15803d',
              marginBottom: '12px'
            }
          }, "Solutions"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Systematic learning approach", "sol1"),
            createListItem("Enhanced preprocessing algorithms", "sol2"),
            createListItem("Modular system design", "sol3"),
            createListItem("Flexible development timeline", "sol4")
          ])
        ])
      ])
    ])
  },
  {
    title: "Future Development",
    icon: createIcon(Lucide.Rocket),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        key: "future-grid",
        style: {
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px'
        }
      }, [
        React.createElement("div", {
          key: "environmental",
          style: {
            padding: '16px',
            backgroundColor: '#eff6ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#1d4ed8',
              marginBottom: '12px'
            }
          }, "Environmental Modeling"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("Room-scale reconstruction", "env1"),
            createListItem("Multiple object handling", "env2"),
            createListItem("Scene understanding", "env3")
          ])
        ]),
        React.createElement("div", {
          key: "cloud",
          style: {
            padding: '16px',
            backgroundColor: '#faf5ff',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#7e22ce',
              marginBottom: '12px'
            }
          }, "Cloud Integration"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("AWS implementation", "cloud1"),
            createListItem("Distributed processing", "cloud2"),
            createListItem("Scalable storage", "cloud3")
          ])
        ]),
        React.createElement("div", {
          key: "advanced",
          style: {
            padding: '16px',
            backgroundColor: '#f0fdf4',
            borderRadius: '12px'
          }
        }, [
          React.createElement("h3", {
            style: {
              fontSize: '1.25rem',
              fontWeight: 'bold',
              color: '#15803d',
              marginBottom: '12px'
            }
          }, "Advanced Features"),
          React.createElement("div", {
            style: { display: 'flex', flexDirection: 'column', gap: '8px' }
          }, [
            createListItem("AI-assisted optimization", "adv1"),
            createListItem("Real-time preview", "adv2"),
            createListItem("Enhanced texture mapping", "adv3")
          ])
        ])
      ])
    ])
  },
  {
    title: "Conclusions",
    icon: createIcon(Lucide.CheckCircle),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '16px'
      }
    }, [
      React.createElement("div", {
        style: {
          padding: '20px',
          backgroundColor: '#f8fafc',
          borderRadius: '12px',
          textAlign: 'center'
        }
      }, [
        React.createElement("h3", {
          style: {
            fontSize: '1.5rem',
            fontWeight: 'bold',
            color: '#1f2937',
            marginBottom: '16px'
          }
        }, "Project Outcomes"),
        React.createElement("div", {
          style: {
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '16px'
          }
        }, [
          React.createElement("div", {
            style: {
              padding: '16px',
              backgroundColor: '#ffffff',
              borderRadius: '8px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }
          }, [
            createListItem("Successfully developed functional 3D reconstruction system", "outcome1"),
            createListItem("Demonstrated adaptability in challenging circumstances", "outcome2"),
            createListItem("Achieved core objectives despite obstacles", "outcome3")
          ]),
          React.createElement("div", {
            style: {
              padding: '16px',
              backgroundColor: '#ffffff',
              borderRadius: '8px',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }
          }, [
            createListItem("Created foundation for future enhancements", "outcome4"),
            createListItem("Established scalable and extensible architecture", "outcome5"),
            createListItem("Delivered production-ready solution", "outcome6")
          ])
        ])
      ])
    ])
  },
  {
    title: "Thank You",
    icon: createIcon(Lucide.Heart),
    content: React.createElement("div", {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '32px',
        alignItems: 'center',
        textAlign: 'center'
      }
    }, [
      React.createElement("h2", {
        style: {
          fontSize: '2.25rem',
          fontWeight: 'bold',
          background: 'linear-gradient(to right, #3b82f6, #8b5cf6)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }
      }, "Questions & Discussion"),
      React.createElement("div", {
        style: {
          marginTop: '16px'
        }
      }, [
        React.createElement("p", {
          style: {
            fontSize: '1.25rem',
            color: '#4b5563',
            marginBottom: '8px'
          }
        }, "Contact:"),
        React.createElement("p", {
          style: {
            fontSize: '1.125rem',
            color: '#6b7280'
          }
        }, "Dor Ferenc"),
        React.createElement("p", {
          style: {
            fontSize: '1.125rem',
            color: '#6b7280'
          }
        }, "Alon Shlomi"),
        React.createElement("p", {
          style: {
            fontSize: '1.125rem',
            color: '#6b7280',
            marginTop: '16px'
          }
        }, "Advisor: Michael Gorelik")
      ])
    ])
  }
];

const nextSlide = () => {
    setCurrentSlide((prev) => Math.min(prev + 1, slides.length - 1));
  };

  const previousSlide = () => {
    setCurrentSlide((prev) => Math.max(prev - 1, 0));
  };

  React.useEffect(() => {
    const handleKeyPress = (e) => {
      if (!isFullscreen) return;

      switch(e.key) {
        case ' ':
        case 'ArrowRight':
        case 'PageDown':
          e.preventDefault();
          nextSlide();
          break;
        case 'ArrowLeft':
        case 'PageUp':
          e.preventDefault();
          previousSlide();
          break;
        case 'Escape':
          setIsFullscreen(false);
          break;
        default:
          break;
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    return () => document.removeEventListener('keydown', handleKeyPress);
  }, [isFullscreen, currentSlide]);

  return React.createElement("div", {
    style: {
      position: isFullscreen ? 'fixed' : 'relative',
      inset: isFullscreen ? 0 : 'auto',
      backgroundColor: '#f9fafb',
      padding: '16px',
      zIndex: isFullscreen ? 50 : 'auto',
      height: isFullscreen ? '100vh' : 'auto'
    }
  }, [
    React.createElement("div", {
      key: "container",
      style: {
        maxWidth: isFullscreen ? '100%' : '1200px',
        margin: '0 auto',
        backgroundColor: 'white',
        borderRadius: '12px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        padding: '16px',
        position: 'relative',
        height: isFullscreen ? '100%' : 'auto'
      }
    }, [
      React.createElement("button", {
        key: "fullscreen",
        onClick: () => setIsFullscreen(!isFullscreen),
        style: {
          position: 'absolute',
          top: '16px',
          right: '16px',
          padding: '8px',
          color: '#4b5563',
          background: 'none',
          border: 'none',
          cursor: 'pointer'
        }
      }, [
        React.createElement(isFullscreen ? Lucide.Minimize2 : Lucide.Maximize2, {
          size: 24
        })
      ]),

      React.createElement("div", {
        key: "content",
        style: {
          height: '800px',
          display: 'flex',
          flexDirection: 'column'
        }
      }, [
        React.createElement("div", {
          key: "header",
          style: {
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            marginBottom: '12px'
          }
        }, [
          slides[currentSlide].icon,
          React.createElement("h1", {
            style: {
              fontSize: '1.875rem',
              fontWeight: 'bold',
              color: '#1f2937'
            }
          }, slides[currentSlide].title)
        ]),

        React.createElement("div", {
          key: "slide-content",
          style: {
            flex: 1,
            overflowY: 'auto',
            marginBottom: '16px'
          }
        }, slides[currentSlide].content),

        React.createElement("div", {
          key: "navigation",
          style: {
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: 'auto',
            paddingTop: '16px'
          }
        }, [
          React.createElement("button", {
            key: "prev",
            onClick: previousSlide,
            disabled: currentSlide === 0,
            style: {
              padding: '8px 16px',
              background: currentSlide === 0 ? '#ccc' : 'linear-gradient(to right, #3b82f6, #2563eb)',
              color: 'white',
              borderRadius: '8px',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              cursor: currentSlide === 0 ? 'not-allowed' : 'pointer',
              opacity: currentSlide === 0 ? 0.5 : 1
            }
          }, [
            React.createElement(Lucide.ChevronLeft, { size: 20 }),
            "Previous"
          ]),

          React.createElement("span", {
            key: "counter",
            style: { color: '#4b5563', fontWeight: 500 }
          }, `${currentSlide + 1} / ${slides.length}`),

          React.createElement("button", {
            key: "next",
            onClick: nextSlide,
            disabled: currentSlide === slides.length - 1,
            style: {
              padding: '8px 16px',
              background: currentSlide === slides.length - 1 ? '#ccc' : 'linear-gradient(to right, #3b82f6, #2563eb)',
              color: 'white',
              borderRadius: '8px',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              cursor: currentSlide === slides.length - 1 ? 'not-allowed' : 'pointer',
              opacity: currentSlide === slides.length - 1 ? 0.5 : 1
            }
          }, [
            "Next",
            React.createElement(Lucide.ChevronRight, { size: 20 })
          ])
        ])
      ])
    ])
  ]);
};

export default Presentation;

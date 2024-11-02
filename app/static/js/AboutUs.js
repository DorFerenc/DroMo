import React from 'react';
import * as Lucide from 'lucide-react';

const AboutUs = () => {
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
        alignItems: 'flex-start',  // Changed from 'top' to 'flex-start'
        gap: '4px',
        marginBottom: '0px',      // Removed bottom margin completely
        lineHeight: '1.2'         // Added to reduce line height
    }
  }, [
    React.createElement("span", {
      key: "bullet",
      style: {
        color: '#3b82f6',
        lineHeight: '1.2'  // Match the line height
    }
    }, "•"),
    React.createElement("span", {
      key: "text",
      style: {
        lineHeight: '1.2'  // Match the line height
      }
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
        }, "Transform Reality into Digital 3D"),
        React.createElement("p", {
          key: "subtitle",
          style: { fontSize: '1.25rem', color: '#4b5563' }
        }, "Automated 3D Reconstruction System"),
        React.createElement("div", {
          key: "credits",
          style: { marginTop: '16px', color: '#374151' }
        }, [
          React.createElement("p", { key: "authors" }, "By: Dor Ferenc & Alon Shlomi"),
          React.createElement("p", { key: "advisor" }, "Advisor: Michael Gorelik")
        ])
      ])
    },
    {
        title: "Overview",
        icon: createIcon(Lucide.Layout),
        content: React.createElement("div", {
          style: {
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '8px'
          }
        }, [
          // Project Scope
          React.createElement("div", {
            key: "scope",
            style: {
              padding: '12px',
              backgroundColor: '#eff6ff',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.125rem',
                fontWeight: 'bold',
                color: '#1d4ed8',
                marginBottom: '6px'
              }
            }, "Project Scope"),
            React.createElement("div", {
              style: { display: 'flex', flexDirection: 'column', gap: '2px' }
            }, [
              createListItem("Automated 3D model generation from LIDAR scans", "scope1"),
              createListItem("Advanced preprocessing pipeline", "scope2"),
              createListItem("Professional-grade output formats", "scope3")
            ])
          ]),
          // Key Features
          React.createElement("div", {
            key: "features",
            style: {
              padding: '12px',
              backgroundColor: '#faf5ff',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.125rem',
                fontWeight: 'bold',
                color: '#7e22ce',
                marginBottom: '6px'
              }
            }, "Key Features"),
            React.createElement("div", {
              style: { display: 'flex', flexDirection: 'column', gap: '2px' }
            }, [
              createListItem("Simplify 3D reconstruction process", "feat1"),
              createListItem("Handle varying quality input data", "feat2"),
              createListItem("Create production-ready 3D models", "feat3")
            ])
          ]),
          // Project Goals
          React.createElement("div", {
            key: "goals",
            style: {
              padding: '12px',
              backgroundColor: '#f0fdf4',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.125rem',
                fontWeight: 'bold',
                color: '#15803d',
                marginBottom: '6px'
              }
            }, "Project Goals"),
            React.createElement("div", {
              style: { display: 'flex', flexDirection: 'column', gap: '2px' }
            }, [
              createListItem("Modular API-first architecture", "goal1"),
              createListItem("Robust noise reduction algorithms", "goal2"),
              createListItem("Industry-standard output formats", "goal3")
            ])
          ])
        ])
      },
      {
        title: "Market Opportunity",
        icon: createIcon(Lucide.Briefcase),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          // Market Size Section
          React.createElement("div", {
            style: {
              padding: '12px',
              background: 'linear-gradient(to right, #eff6ff, #faf5ff)',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                marginBottom: '16px'
              }
            }, "3D Scanning Market Size"),
            React.createElement("div", {
              style: {
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '8px'
              }
            }, [
              React.createElement("div", {
                key: "market",
                style: {
                    backgroundColor: 'white',
                    padding: '16px',
                    borderRadius: '8px',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'flex-start',
                    gap: '4px'
                }
              }, [
                React.createElement("p", {
                  style: {
                    fontSize: '1.875rem',
                    fontWeight: 'bold',
                    color: '#2563eb'
                  }
                }, "$4.7B"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Current Market Size")
              ]),
              React.createElement("div", {
                key: "growth",
                style: {
                    backgroundColor: 'white',
                    padding: '16px',
                    borderRadius: '8px',
                    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                    display: 'flex',
                    flexDirection: 'column',  // Changed to column
                    alignItems: 'flex-start', // Align to the left
                    gap: '4px'
                }
              }, [
                React.createElement("p", {
                  style: {
                    fontSize: '1.875rem',
                    fontWeight: 'bold',
                    color: '#16a34a'
                  }
                }, "16.3%"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Annual Growth Rate")
              ])
            ])
          ]),
          // Industries and Edge Section
          React.createElement("div", {
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "industries",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
          }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Target Industries"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Manufacturing & Engineering", "ind1"),
                createListItem("Architecture & Construction", "ind2"),
                createListItem("Cultural Heritage", "ind3"),
                createListItem("E-commerce & Retail", "ind4")
              ])
            ]),
            React.createElement("div", {
              key: "edge",
              style: {
                padding: '12px',
                backgroundColor: '#faf5ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#7e22ce',
                  marginBottom: '6px'
                }
              }, "Competitive Edge"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Lower cost than existing solutions", "edge1"),
                createListItem("Faster processing time", "edge2"),
                createListItem("More user-friendly interface", "edge3"),
                createListItem("Works with consumer hardware", "edge4")
              ])
            ])
          ])
        ])
      },
      {
        title: "The Challenge",
        icon: createIcon(Lucide.Target),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "challenges",
              style: {
                padding: '12px',
                backgroundColor: '#fef2f2',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#dc2626',
                  marginBottom: '6px'
                }
              }, "Industry Challenges"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("High-quality 3D reconstruction requires expensive equipment", "ch1"),
                createListItem("Processing noisy scan data is complex", "ch2"),
                createListItem("Existing solutions lack flexibility", "ch3"),
                createListItem("High barrier to entry", "ch4")
              ])
            ]),
            React.createElement("div", {
              key: "hurdles",
              style: {
                padding: '12px',
                backgroundColor: '#fff7ed',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#ea580c',
                  marginBottom: '6px'
                }
              }, "Technical Hurdles"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Noise in scan data", "th1"),
                createListItem("Missing geometric information", "th2"),
                createListItem("Inconsistent point cloud density", "th3"),
                createListItem("Complex surface reconstruction", "th4")
              ])
            ])
          ])
        ])
      },
      {
        title: "DroMo Solution",
        icon: createIcon(Lucide.Cpu),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "approach",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Our Approach"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("End-to-end processing pipeline", "app1"),
                createListItem("Advanced noise reduction algorithms", "app2"),
                createListItem("Intelligent surface reconstruction", "app3"),
                createListItem("Automated texture mapping", "app4")
              ])
            ]),
            React.createElement("div", {
              key: "innovations",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginBottom: '6px'
                }
              }, "Key Innovations"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Robust preprocessing for low-quality scans", "inn1"),
                createListItem("Modular, maintainable architecture", "inn2"),
                createListItem("API-first design for flexible integration", "inn3"),
                createListItem("Streamlined user workflow", "inn4")
              ])
            ])
          ])
        ])
      },
      {
        title: "Evolution",
        icon: createIcon(Lucide.Globe),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "initial",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Initial Approach"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Video-based input source", "init1"),
                createListItem("Structure from Motion (SfM)", "init2"),
                createListItem("Point cloud generation from video frames", "init3")
              ])
            ]),
            React.createElement("div", {
              key: "current",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginBottom: '6px'
                }
              }, "Current System"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("LIDAR scan input", "curr1"),
                createListItem("Enhanced preprocessing pipeline", "curr2"),
                createListItem("Robust reconstruction algorithms", "curr3"),
                createListItem("Modular architecture advantages", "curr4")
              ])
            ])
          ]),
          React.createElement("div", {
            style: {
              padding: '12px',
              backgroundColor: '#faf5ff',
              borderRadius: '8px'
            }
          }, [
            React.createElement("div", {
              style: {
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }
            }, [
              React.createElement("div", {
                key: "challenge",
                style: {
                  textAlign: 'center',
                  flex: 1
                }
              }, [
                React.createElement("h4", {
                  style: {
                    fontWeight: 'bold',
                    color: '#dc2626'
                  }
                }, "Challenge"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Inconsistent point cloud quality")
              ]),
              React.createElement("div", {
                key: "solution",
                style: {
                  textAlign: 'center',
                  flex: 1
                }
              }, [
                React.createElement("h4", {
                  style: {
                    fontWeight: 'bold',
                    color: '#2563eb'
                  }
                }, "Solution"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Switch to LIDAR scanning")
              ])
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
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "grid-section",
            style: {
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "ui-section",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                key: "ui-title",
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "User Interface"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Web Application", "ui-1"),
                createListItem("Direct API Access", "ui-2"),
                createListItem("Data Management", "ui-3")
              ])
            ]),
            React.createElement("div", {
              key: "pipeline-section",
              style: {
                padding: '12px',
                backgroundColor: '#faf5ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                key: "pipeline-title",
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#7e22ce',
                  marginBottom: '6px'
                }
              }, "Processing Pipeline"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Algorithm Implementation", "pipeline-1"),
                createListItem("Progress Tracking", "pipeline-2"),
                createListItem("Error Handling", "pipeline-3")
              ])
            ]),
            React.createElement("div", {
              key: "core-section",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                key: "core-title",
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginBottom: '6px'
                }
              }, "Core Services"),
              React.createElement("div", {
                style: { display: 'flex', flexDirection: 'column', gap: '2px' }
              }, [
                createListItem("Input Handler", "core-1"),
                createListItem("Preprocessor", "core-2"),
                createListItem("Reconstructor", "core-3")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "data-flow",
            style: {
              padding: '12px',
              background: 'linear-gradient(to right, #eff6ff, #faf5ff)',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              key: "flow-title",
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                marginBottom: '8px'
              }
            }, "Data Flow"),
            React.createElement("div", {
              key: "flow-content",
              style: {
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '8px'
              }
            }, [
              React.createElement("div", {
                key: "input",
                style: {
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  key: "input-title",
                  style: {
                    fontWeight: 'bold',
                    color: '#2563eb'
                  }
                }, "Input"),
                React.createElement("p", {
                  key: "input-desc",
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "LIDAR Data")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-1",
                style: { color: '#9ca3af' }
              }),
              React.createElement("div", {
                key: "processing",
                style: {
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  key: "processing-title",
                  style: {
                    fontWeight: 'bold',
                    color: '#7e22ce'
                  }
                }, "Processing"),
                React.createElement("p", {
                  key: "processing-desc",
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Pipeline Stages")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-2",
                style: { color: '#9ca3af' }
              }),
              React.createElement("div", {
                key: "output",
                style: {
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  key: "output-title",
                  style: {
                    fontWeight: 'bold',
                    color: '#16a34a'
                  }
                }, "Output"),
                React.createElement("p", {
                  key: "output-desc",
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "3D Model")
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
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "tech-grid",
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "core-tech",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                key: "core-tech-title",
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Core Technologies"),
              React.createElement("div", {
                key: "core-tech-items",
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }
              }, [
                // Tech items with white background boxes
                ...["Backend: Python", "API Framework: Flask", "Database: MongoDB", "Containerization: Docker"]
                  .map((tech, index) => React.createElement("div", {
                    key: `tech-${index}`,
                    style: {
                      backgroundColor: 'white',
                      padding: '8px',
                      borderRadius: '6px'
                    }
                  }, [
                    React.createElement("p", {
                      style: { fontWeight: 'bold' }
                    }, tech),
                    React.createElement("p", {
                      style: {
                        fontSize: '0.875rem',
                        color: '#4b5563'
                      }
                    }, "Primary development language")
                  ]))
              ])
            ]),
            React.createElement("div", {
              key: "right-column",
              style: {
                display: 'flex',
                flexDirection: 'column',
                gap: '8px'
              }
            }, [
              React.createElement("div", {
                key: "processing-libs",
                style: {
                  padding: '12px',
                  backgroundColor: '#faf5ff',
                  borderRadius: '8px'
                }
              }, [
                React.createElement("h3", {
                  style: {
                    fontSize: '1.125rem',
                    fontWeight: 'bold',
                    color: '#7e22ce',
                    marginBottom: '6px'
                  }
                }, "Processing Libraries"),
                React.createElement("div", {
                  style: { display: 'flex', flexDirection: 'column', gap: '2px' }
                }, [
                  createListItem("3D Processing: Open3D", "lib-1"),
                  createListItem("Scientific Computing: NumPy/SciPy", "lib-2"),
                  createListItem("Visualization: PyVista", "lib-3")
                ])
              ]),
              React.createElement("div", {
                key: "dev-tools",
                style: {
                  padding: '12px',
                  backgroundColor: '#f0fdf4',
                  borderRadius: '8px'
                }
              }, [
                React.createElement("h3", {
                  style: {
                    fontSize: '1.125rem',
                    fontWeight: 'bold',
                    color: '#15803d',
                    marginBottom: '6px'
                  }
                }, "Development Tools"),
                React.createElement("div", {
                  style: { display: 'flex', flexDirection: 'column', gap: '2px' }
                }, [
                  createListItem("Version Control: Git", "tool-1"),
                  createListItem("Testing: PyTest", "tool-2"),
                  createListItem("CI/CD Pipeline", "tool-3")
                ])
              ])
            ])
          ])
        ])
      },
      {
        title: "Processing Pipeline",
        icon: createIcon(Lucide.Settings),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "pipeline-stages",
            style: {
              padding: '12px',
              background: 'linear-gradient(to right, #eff6ff, #faf5ff)',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              key: "stages-title",
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                marginBottom: '8px'
              }
            }, "Pipeline Stages"),
            React.createElement("div", {
              key: "stages-flow",
              style: {
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: '8px'
              }
            }, [
              React.createElement("div", {
                key: "stage-1",
                style: {
                  flex: 1,
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  style: {
                    fontWeight: 'bold',
                    color: '#2563eb'
                  }
                }, "1. Point Cloud Processing"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Data cleaning and optimization")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-1",
                style: { color: '#9ca3af' }
              }),
              React.createElement("div", {
                key: "stage-2",
                style: {
                  flex: 1,
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  style: {
                    fontWeight: 'bold',
                    color: '#7e22ce'
                  }
                }, "2. Mesh Generation"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Surface reconstruction")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-2",
                style: { color: '#9ca3af' }
              }),
              React.createElement("div", {
                key: "stage-3",
                style: {
                  flex: 1,
                  backgroundColor: 'white',
                  padding: '8px',
                  borderRadius: '8px',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                  textAlign: 'center'
                }
              }, [
                React.createElement("p", {
                  style: {
                    fontWeight: 'bold',
                    color: '#16a34a'
                  }
                }, "3. Texture Mapping"),
                React.createElement("p", {
                  style: {
                    fontSize: '0.875rem',
                    color: '#4b5563'
                  }
                }, "Visual enhancement")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "details-grid",
            style: {
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "point-cloud",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Point Cloud Processing"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Statistical Outlier Removal", "pc-1"),
                createListItem("Voxel Downsampling", "pc-2"),
                createListItem("Normal Estimation", "pc-3"),
                createListItem("Background Removal", "pc-4")
              ])
            ]),
            React.createElement("div", {
              key: "mesh-gen",
              style: {
                padding: '12px',
                backgroundColor: '#faf5ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#7e22ce',
                  marginBottom: '6px'
                }
              }, "Mesh Generation"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Alpha Shape Computation", "mesh-1"),
                createListItem("Delaunay Triangulation", "mesh-2"),
                createListItem("Topology Verification", "mesh-3"),
                createListItem("Surface Optimization", "mesh-4")
              ])
            ]),
            React.createElement("div", {
              key: "texture",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginBottom: '6px'
                }
              }, "Texture Mapping"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("UV Coordinate Generation", "texture-1"),
                createListItem("Color Assignment", "texture-2"),
                createListItem("Texture Atlas Creation", "texture-3"),
                createListItem("Quality Enhancement", "texture-4")
              ])
            ])
          ])
        ]),
      },
      {
        title: "Results & Performance",
        icon: createIcon(Lucide.BarChart),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "metrics",
            style: {
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "success",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px',
                textAlign: 'center'
              }
            }, [
              React.createElement("p", {
                style: {
                  fontSize: '1.875rem',
                  fontWeight: 'bold',
                  color: '#2563eb'
                }
              }, "90%+"),
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginTop: '4px'
                }
              }, "Success Rate"),
              React.createElement("p", {
                style: {
                  fontSize: '0.875rem',
                  color: '#4b5563',
                  marginTop: '4px'
                }
              }, "Successful model generation from valid scans")
            ]),
            React.createElement("div", {
              key: "processing",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px',
                textAlign: 'center'
              }
            }, [
              React.createElement("p", {
                style: {
                  fontSize: '1.875rem',
                  fontWeight: 'bold',
                  color: '#16a34a'
                }
              }, "4-25s"),
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginTop: '4px'
                }
              }, "Processing Time"),
              React.createElement("p", {
                style: {
                  fontSize: '0.875rem',
                  color: '#4b5563',
                  marginTop: '4px'
                }
              }, "Based on input complexity")
            ]),
            React.createElement("div", {
              key: "noise",
              style: {
                padding: '12px',
                backgroundColor: '#faf5ff',
                borderRadius: '8px',
                textAlign: 'center'
              }
            }, [
              React.createElement("p", {
                style: {
                  fontSize: '1.875rem',
                  fontWeight: 'bold',
                  color: '#7e22ce'
                }
              }, "60%"),
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#7e22ce',
                  marginTop: '4px'
                }
              }, "Noise Reduction"),
              React.createElement("p", {
                style: {
                  fontSize: '0.875rem',
                  color: '#4b5563',
                  marginTop: '4px'
                }
              }, "Average point cloud optimization")
            ])
          ]),
          React.createElement("div", {
            key: "details",
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "performance",
              style: {
                padding: '12px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#374151',
                  marginBottom: '6px'
                }
              }, "Performance Metrics"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }
              }, [
                ...["Small Files (200K-400K points)", "Medium Files (400K-1M points)", "Large Files (1M-3M points)"]
                  .map((label, index) => React.createElement("div", {
                    key: `perf-${index}`,
                    style: {
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }
                  }, [
                    React.createElement("span", {
                      style: { color: '#4b5563' }
                    }, label),
                    React.createElement("span", {
                      style: {
                        fontWeight: 'bold',
                        color: index === 0 ? '#16a34a' : index === 1 ? '#2563eb' : '#7e22ce'
                      }
                    }, [`4s`, `14s`, `25s`][index])
                  ]))
              ])
            ]),
            React.createElement("div", {
              key: "quality",
              style: {
                padding: '12px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#374151',
                  marginBottom: '6px'
                }
              }, "Quality Metrics"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px'
                }
              }, [
                ...["Mesh Quality Score", "Texture Quality", "Overall Appearance"]
                  .map((label, index) => React.createElement("div", {
                    key: `quality-${index}`,
                    style: {
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center'
                    }
                  }, [
                    React.createElement("span", {
                      style: { color: '#4b5563' }
                    }, label),
                    React.createElement("span", {
                      style: {
                        fontWeight: 'bold',
                        color: index === 0 ? '#16a34a' : index === 1 ? '#2563eb' : '#7e22ce'
                      }
                    }, [`9.3/10`, `9.5/10`, `9.0/10`][index])
                  ]))
              ])
            ])
          ])
        ])
      },
      {
        title: "Real-World Impact",
        icon: createIcon(Lucide.Target),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "main-content",
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "use-cases",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '8px'
                }
              }, "Use Cases"),
              React.createElement("div", {
                key: "cases",
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }
              }, [
                ...["Product Design", "Cultural Heritage", "Education"].map((title, index) =>
                  React.createElement("div", {
                    key: `case${index + 1}`,
                    style: {
                      backgroundColor: 'white',
                      padding: '8px',
                      borderRadius: '8px'
                    }
                  }, [
                    React.createElement("h4", {
                      style: { fontWeight: 'bold' }
                    }, title),
                    React.createElement("p", {
                      style: {
                        fontSize: '0.875rem',
                        color: '#4b5563'
                      }
                    }, [
                      "40% reduction in prototyping time",
                      "Digital preservation of artifacts",
                      "Enhanced 3D learning resources"
                    ][index])
                  ])
                )
              ])
            ]),
            React.createElement("div", {
              key: "benefits",
              style: {
                padding: '12px',
                backgroundColor: '#f0fdf4',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#15803d',
                  marginBottom: '8px'
                }
              }, "Key Benefits"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Cost reduction vs traditional methods", "benefit1"),
                createListItem("Accelerated design processes", "benefit2"),
                createListItem("Improved accessibility to 3D scanning", "benefit3"),
                createListItem("Reduced environmental impact", "benefit4"),
                createListItem("Enhanced collaboration capabilities", "benefit5")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "achievements",
            style: {
              padding: '12px',
              backgroundColor: '#faf5ff',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.125rem',
                fontWeight: 'bold',
                color: '#7e22ce',
                marginBottom: '8px'
              }
            }, "Achievements"),
            React.createElement("div", {
              key: "stats",
              style: {
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '8px'
              }
            }, [
              ...["Cost Reduction", "Time Saved", "User Satisfaction"].map((label, index) =>
                React.createElement("div", {
                  key: label.toLowerCase().replace(" ", "-"),
                  style: { textAlign: 'center' }
                }, [
                  React.createElement("p", {
                    style: {
                      fontSize: '1.5rem',
                      fontWeight: 'bold',
                      color: '#7e22ce'
                    }
                  }, ["60%", "40%", "90%"][index]),
                  React.createElement("p", {
                    style: {
                      fontSize: '0.875rem',
                      color: '#4b5563'
                    }
                  }, label)
                ])
              )
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
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "overview",
            style: {
              padding: '12px',
              background: 'linear-gradient(to right, #eff6ff, #faf5ff)',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.25rem',
                fontWeight: 'bold',
                marginBottom: '8px'
              }
            }, "Demo Overview"),
            React.createElement("div", {
              key: "steps",
              style: {
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '8px'
              }
            }, [
              ...["Input", "Processing", "Output"].map((title, index) =>
                React.createElement("div", {
                  key: title.toLowerCase(),
                  style: {
                    backgroundColor: 'white',
                    padding: '8px',
                    borderRadius: '8px',
                    textAlign: 'center'
                  }
                }, [
                  React.createElement("p", {
                    style: {
                      fontWeight: 'bold',
                      color: index === 0 ? '#2563eb' : index === 1 ? '#7e22ce' : '#16a34a'
                    }
                  }, title),
                  React.createElement("p", {
                    style: {
                      fontSize: '0.875rem',
                      color: '#4b5563'
                    }
                  }, [
                    "LIDAR Scan Data",
                    "Real-time Pipeline",
                    "3D Model Generation"
                  ][index])
                ])
              )
            ])
          ]),
          React.createElement("div", {
            key: "details",
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "features",
              style: {
                padding: '12px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#374151',
                  marginBottom: '6px'
                }
              }, "Key Features Demo"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("File upload and processing", "feature1"),
                createListItem("Real-time progress tracking", "feature2"),
                createListItem("Interactive 3D visualization", "feature3"),
                createListItem("Export functionality", "feature4")
              ])
            ]),
            React.createElement("div", {
              key: "objects",
              style: {
                padding: '12px',
                backgroundColor: '#f9fafb',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#374151',
                  marginBottom: '6px'
                }
              }, "Demo Objects"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Simple geometric shapes", "obj1"),
                createListItem("Complex surface objects", "obj2"),
                createListItem("Textured items", "obj3"),
                createListItem("Various size demonstrations", "obj4")
              ])
            ])
          ])
        ])
      },
      {
        title: "Future Vision",
        icon: createIcon(Lucide.Globe),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px'
          }
        }, [
          React.createElement("div", {
            key: "goals",
            style: {
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '8px'
            }
          }, [
            React.createElement("div", {
              key: "short-term",
              style: {
                padding: '12px',
                backgroundColor: '#eff6ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#1d4ed8',
                  marginBottom: '6px'
                }
              }, "Short-term Goals"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Cloud integration (AWS)", "goal1"),
                createListItem("Mobile application development", "goal2"),
                createListItem("Enhanced preprocessing algorithms", "goal3"),
                createListItem("Advanced texture mapping", "goal4")
              ])
            ]),
            React.createElement("div", {
              key: "long-term",
              style: {
                padding: '12px',
                backgroundColor: '#faf5ff',
                borderRadius: '8px'
              }
            }, [
              React.createElement("h3", {
                style: {
                  fontSize: '1.125rem',
                  fontWeight: 'bold',
                  color: '#7e22ce',
                  marginBottom: '6px'
                }
              }, "Long-term Vision"),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("AI-powered optimization", "vision1"),
                createListItem("Real-time reconstruction", "vision2"),
                createListItem("Multi-object scanning", "vision3"),
                createListItem("Industry-standard integration", "vision4")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "research",
            style: {
              padding: '12px',
              backgroundColor: '#f0fdf4',
              borderRadius: '8px'
            }
          }, [
            React.createElement("h3", {
              style: {
                fontSize: '1.125rem',
                fontWeight: 'bold',
                color: '#15803d',
                marginBottom: '6px'
              }
            }, "Research Directions"),
            React.createElement("div", {
              key: "directions",
              style: {
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '8px'
              }
            }, [
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Advanced ML algorithms", "research1"),
                createListItem("Environmental modeling", "research2"),
                createListItem("Automated parameter tuning", "research3")
              ]),
              React.createElement("div", {
                style: {
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }
              }, [
                createListItem("Enhanced geometry processing", "research4"),
                createListItem("Large-scale reconstruction", "research5"),
                createListItem("Real-time optimization", "research6")
              ])
            ])
          ])
        ])
      },
      {
        title: "Thank You",
        icon: createIcon(Lucide.Award),
        content: React.createElement("div", {
          style: {
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
            textAlign: 'center'
          }
        }, [
          React.createElement("h2", {
            style: {
              fontSize: '1.875rem',
              fontWeight: 'bold',
              background: 'linear-gradient(to right, #3b82f6, #8b5cf6)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }
          }, "Ready for Questions"),
          React.createElement("p", {
            style: {
              fontSize: '1.25rem',
              color: '#4b5563'
            }
          }, "Thank you for your attention"),
          React.createElement("div", {
            style: {
              marginTop: '16px'
            }
          }, [
            React.createElement("div", {
              style: {
                padding: '12px',
                background: 'linear-gradient(to right, #eff6ff, #faf5ff)',
                borderRadius: '8px'
              }
            }, [
              React.createElement("p", {
                style: {
                  fontSize: '1.125rem',
                  color: '#374151'
                }
              }, "DroMo Project"),
              React.createElement("p", {
                style: {
                  color: '#4b5563'
                }
              }, "Transforming Reality into Digital 3D")
            ])
          ])
        ])
      }
    // Add other slides here following the same pattern
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

export default AboutUs;
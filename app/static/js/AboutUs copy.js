import React, { createElement, useState, useEffect } from 'react';
import * as Lucide from 'lucide-react';

const AboutUs = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const createIcon = (IconComponent) => React.createElement(IconComponent, {
    size: 48,
    className: "text-blue-500"
  });

const createListItem = (text, key) => React.createElement("p", {
    key,
    className: "text-xl text-gray-600 flex items-center space-x-2"
  }, [
    React.createElement("span", {
      key: "bullet",
      className: "text-blue-500"
    }, "•"),
    React.createElement("span", {
      key: "text"
    }, text)
  ]);


  const slides = [
    {
      title: "DroMo",
      icon: createIcon(Lucide.Box),
      content: React.createElement("div", {
        className: "space-y-6 text-center"
      }, [
        React.createElement("h2", {
          key: "title",
          className: "text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text"
        }, "Transform Reality into Digital 3D"),
        React.createElement("p", {
          key: "subtitle",
          className: "text-xl text-gray-600"
        }, "Automated 3D Reconstruction System"),
        React.createElement("div", {
          key: "credits",
          className: "mt-8 space-y-2 text-gray-700"
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
        className: "space-y-6"
      }, [
        React.createElement("div", {
          className: "grid grid-cols-3 gap-6"
        }, [
          // Project Scope
          React.createElement("div", {
            key: "scope",
            className: "bg-blue-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-blue-700 mb-3"
            }, "Project Scope"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("Automated 3D model generation from LIDAR scans", "scope1"),
              createListItem("Advanced preprocessing pipeline", "scope2"),
              createListItem("Professional-grade output formats", "scope3")
            ])
          ]),
          // Key Features
          React.createElement("div", {
            key: "features",
            className: "bg-purple-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-purple-700 mb-3"
            }, "Key Features"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("Simplify 3D reconstruction process", "feat1"),
              createListItem("Handle varying quality input data", "feat2"),
              createListItem("Create production-ready 3D models", "feat3")
            ])
          ]),
          // Project Goals
          React.createElement("div", {
            key: "goals",
            className: "bg-green-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-green-700 mb-3"
            }, "Project Goals"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("Modular API-first architecture", "goal1"),
              createListItem("Robust noise reduction algorithms", "goal2"),
              createListItem("Industry-standard output formats", "goal3")
            ])
          ])
        ])
      ])
    },
    {
      title: "Market Opportunity",
      icon: createIcon(Lucide.Briefcase),
      content: React.createElement("div", {
        className: "space-y-6"
      }, [
        // Market Size Section
        React.createElement("div", {
          className: "bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg"
        }, [
          React.createElement("h3", {
            className: "text-xl font-bold mb-4"
          }, "3D Scanning Market Size"),
          React.createElement("div", {
            className: "grid grid-cols-2 gap-6"
          }, [
            React.createElement("div", {
              key: "market",
              className: "bg-white p-4 rounded-lg shadow-sm"
            }, [
              React.createElement("p", {
                className: "text-3xl font-bold text-blue-600"
              }, "$4.7B"),
              React.createElement("p", {
                className: "text-sm text-gray-600"
              }, "Current Market Size")
            ]),
            React.createElement("div", {
              key: "growth",
              className: "bg-white p-4 rounded-lg shadow-sm"
            }, [
              React.createElement("p", {
                className: "text-3xl font-bold text-green-600"
              }, "16.3%"),
              React.createElement("p", {
                className: "text-sm text-gray-600"
              }, "Annual Growth Rate")
            ])
          ])
        ]),
        // Industries and Edge Section
        React.createElement("div", {
          className: "grid grid-cols-2 gap-6"
        }, [
          React.createElement("div", {
            key: "industries",
            className: "bg-blue-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-blue-700 mb-3"
            }, "Target Industries"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("Manufacturing & Engineering", "ind1"),
              createListItem("Architecture & Construction", "ind2"),
              createListItem("Cultural Heritage", "ind3"),
              createListItem("E-commerce & Retail", "ind4")
            ])
          ]),
          React.createElement("div", {
            key: "edge",
            className: "bg-purple-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-purple-700 mb-3"
            }, "Competitive Edge"),
            React.createElement("div", {
              className: "space-y-3"
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
        className: "space-y-6"
      }, [
        React.createElement("div", {
          className: "grid grid-cols-2 gap-6"
        }, [
          React.createElement("div", {
            key: "challenges",
            className: "bg-red-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-red-700 mb-3"
            }, "Industry Challenges"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("High-quality 3D reconstruction requires expensive equipment", "ch1"),
              createListItem("Processing noisy scan data is complex", "ch2"),
              createListItem("Existing solutions lack flexibility", "ch3"),
              createListItem("High barrier to entry", "ch4")
            ])
          ]),
          React.createElement("div", {
            key: "hurdles",
            className: "bg-orange-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-orange-700 mb-3"
            }, "Technical Hurdles"),
            React.createElement("div", {
              className: "space-y-3"
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
        className: "space-y-6"
      }, [
        React.createElement("div", {
          className: "grid grid-cols-2 gap-6"
        }, [
          React.createElement("div", {
            key: "approach",
            className: "bg-blue-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-blue-700 mb-3"
            }, "Our Approach"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("End-to-end processing pipeline", "app1"),
              createListItem("Advanced noise reduction algorithms", "app2"),
              createListItem("Intelligent surface reconstruction", "app3"),
              createListItem("Automated texture mapping", "app4")
            ])
          ]),
          React.createElement("div", {
            key: "innovations",
            className: "bg-green-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-green-700 mb-3"
            }, "Key Innovations"),
            React.createElement("div", {
              className: "space-y-3"
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
        className: "space-y-6"
      }, [
        React.createElement("div", {
          className: "grid grid-cols-2 gap-6"
        }, [
          React.createElement("div", {
            key: "initial",
            className: "bg-blue-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-blue-700 mb-3"
            }, "Initial Approach"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("Video-based input source", "init1"),
              createListItem("Structure from Motion (SfM)", "init2"),
              createListItem("Point cloud generation from video frames", "init3")
            ])
          ]),
          React.createElement("div", {
            key: "current",
            className: "bg-green-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              className: "text-lg font-bold text-green-700 mb-3"
            }, "Current System"),
            React.createElement("div", {
              className: "space-y-3"
            }, [
              createListItem("LIDAR scan input", "curr1"),
              createListItem("Enhanced preprocessing pipeline", "curr2"),
              createListItem("Robust reconstruction algorithms", "curr3"),
              createListItem("Modular architecture advantages", "curr4")
            ])
          ])
        ]),
        React.createElement("div", {
          className: "bg-purple-50 p-6 rounded-lg"
        }, [
          React.createElement("div", {
            className: "flex justify-between items-center"
          }, [
            React.createElement("div", {
              key: "challenge",
              className: "text-center flex-1"
            }, [
              React.createElement("h4", {
                className: "font-bold text-red-600"
              }, "Challenge"),
              React.createElement("p", {
                className: "text-sm text-gray-600"
              }, "Inconsistent point cloud quality")
            ]),
            React.createElement("div", {
              key: "solution",
              className: "text-center flex-1"
            }, [
              React.createElement("h4", {
                className: "font-bold text-blue-600"
              }, "Solution"),
              React.createElement("p", {
                className: "text-sm text-gray-600"
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
          className: "space-y-6"
        }, [
          React.createElement("div", {
            key: "grid-section",
            className: "grid grid-cols-3 gap-6"
          }, [
            React.createElement("div", {
              key: "ui-section",
              className: "bg-blue-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "ui-title",
                className: "text-lg font-bold text-blue-700 mb-3"
              }, "User Interface"),
              React.createElement("ul", {
                key: "ui-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("Web Application", "ui-1"),
                createListItem("Direct API Access", "ui-2"),
                createListItem("Data Management", "ui-3")
              ])
            ]),
            React.createElement("div", {
              key: "pipeline-section",
              className: "bg-purple-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "pipeline-title",
                className: "text-lg font-bold text-purple-700 mb-3"
              }, "Processing Pipeline"),
              React.createElement("ul", {
                key: "pipeline-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("Algorithm Implementation", "pipeline-1"),
                createListItem("Progress Tracking", "pipeline-2"),
                createListItem("Error Handling", "pipeline-3")
              ])
            ]),
            React.createElement("div", {
              key: "core-section",
              className: "bg-green-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "core-title",
                className: "text-lg font-bold text-green-700 mb-3"
              }, "Core Services"),
              React.createElement("ul", {
                key: "core-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("Input Handler", "core-1"),
                createListItem("Preprocessor", "core-2"),
                createListItem("Reconstructor", "core-3")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "data-flow",
            className: "bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              key: "flow-title",
              className: "text-xl font-bold mb-4"
            }, "Data Flow"),
            React.createElement("div", {
              key: "flow-content",
              className: "flex justify-between items-center space-x-4"
            }, [
              React.createElement("div", {
                key: "input",
                className: "bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "input-title",
                  className: "font-bold text-blue-600"
                }, "Input"),
                React.createElement("p", {
                  key: "input-desc",
                  className: "text-sm text-gray-600"
                }, "LIDAR Data")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-1",
                className: "text-gray-400"
              }),
              React.createElement("div", {
                key: "processing",
                className: "bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "processing-title",
                  className: "font-bold text-purple-600"
                }, "Processing"),
                React.createElement("p", {
                  key: "processing-desc",
                  className: "text-sm text-gray-600"
                }, "Pipeline Stages")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-2",
                className: "text-gray-400"
              }),
              React.createElement("div", {
                key: "output",
                className: "bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "output-title",
                  className: "font-bold text-green-600"
                }, "Output"),
                React.createElement("p", {
                  key: "output-desc",
                  className: "text-sm text-gray-600"
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
          className: "space-y-6"
        }, [
          React.createElement("div", {
            key: "tech-grid",
            className: "grid grid-cols-2 gap-6"
          }, [
            React.createElement("div", {
              key: "core-tech",
              className: "bg-blue-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "core-tech-title",
                className: "text-lg font-bold text-blue-700 mb-3"
              }, "Core Technologies"),
              React.createElement("div", {
                key: "core-tech-items",
                className: "space-y-3"
              }, [
                React.createElement("div", {
                  key: "tech-1",
                  className: "bg-white p-3 rounded"
                }, [
                  React.createElement("p", {
                    key: "tech-1-title",
                    className: "font-bold"
                  }, "Backend: Python"),
                  React.createElement("p", {
                    key: "tech-1-desc",
                    className: "text-sm text-gray-600"
                  }, "Primary development language")
                ]),
                React.createElement("div", {
                  key: "tech-2",
                  className: "bg-white p-3 rounded"
                }, [
                  React.createElement("p", {
                    key: "tech-2-title",
                    className: "font-bold"
                  }, "API Framework: Flask"),
                  React.createElement("p", {
                    key: "tech-2-desc",
                    className: "text-sm text-gray-600"
                  }, "RESTful API implementation")
                ]),
                React.createElement("div", {
                  key: "tech-3",
                  className: "bg-white p-3 rounded"
                }, [
                  React.createElement("p", {
                    key: "tech-3-title",
                    className: "font-bold"
                  }, "Database: MongoDB"),
                  React.createElement("p", {
                    key: "tech-3-desc",
                    className: "text-sm text-gray-600"
                  }, "Data persistence layer")
                ]),
                React.createElement("div", {
                  key: "tech-4",
                  className: "bg-white p-3 rounded"
                }, [
                  React.createElement("p", {
                    key: "tech-4-title",
                    className: "font-bold"
                  }, "Containerization: Docker"),
                  React.createElement("p", {
                    key: "tech-4-desc",
                    className: "text-sm text-gray-600"
                  }, "Deployment and scaling")
                ])
              ])
            ]),
            React.createElement("div", {
              key: "right-column",
              className: "space-y-6"
            }, [
              React.createElement("div", {
                key: "processing-libs",
                className: "bg-purple-50 p-6 rounded-lg"
              }, [
                React.createElement("h3", {
                  key: "libs-title",
                  className: "text-lg font-bold text-purple-700 mb-3"
                }, "Processing Libraries"),
                React.createElement("ul", {
                  key: "libs-list",
                  className: "space-y-2 text-gray-600"
                }, [
                  createListItem("3D Processing: Open3D", "lib-1"),
                  createListItem("Scientific Computing: NumPy/SciPy", "lib-2"),
                  createListItem("Visualization: PyVista", "lib-3")
                ])
              ]),
              React.createElement("div", {
                key: "dev-tools",
                className: "bg-green-50 p-6 rounded-lg"
              }, [
                React.createElement("h3", {
                  key: "tools-title",
                  className: "text-lg font-bold text-green-700 mb-3"
                }, "Development Tools"),
                React.createElement("ul", {
                  key: "tools-list",
                  className: "space-y-2 text-gray-600"
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
          className: "space-y-6"
        }, [
          React.createElement("div", {
            key: "pipeline-stages",
            className: "bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg"
          }, [
            React.createElement("h3", {
              key: "stages-title",
              className: "text-xl font-bold mb-4"
            }, "Pipeline Stages"),
            React.createElement("div", {
              key: "stages-flow",
              className: "flex justify-between items-center space-x-4"
            }, [
              React.createElement("div", {
                key: "stage-1",
                className: "flex-1 bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "stage-1-title",
                  className: "font-bold text-blue-600"
                }, "1. Point Cloud Processing"),
                React.createElement("p", {
                  key: "stage-1-desc",
                  className: "text-sm text-gray-600"
                }, "Data cleaning and optimization")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-1",
                className: "text-gray-400"
              }),
              React.createElement("div", {
                key: "stage-2",
                className: "flex-1 bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "stage-2-title",
                  className: "font-bold text-purple-600"
                }, "2. Mesh Generation"),
                React.createElement("p", {
                  key: "stage-2-desc",
                  className: "text-sm text-gray-600"
                }, "Surface reconstruction")
              ]),
              React.createElement(Lucide.ChevronRight, {
                key: "arrow-2",
                className: "text-gray-400"
              }),
              React.createElement("div", {
                key: "stage-3",
                className: "flex-1 bg-white p-4 rounded-lg shadow-sm text-center"
              }, [
                React.createElement("p", {
                  key: "stage-3-title",
                  className: "font-bold text-green-600"
                }, "3. Texture Mapping"),
                React.createElement("p", {
                  key: "stage-3-desc",
                  className: "text-sm text-gray-600"
                }, "Visual enhancement")
              ])
            ])
          ]),
          React.createElement("div", {
            key: "details-grid",
            className: "grid grid-cols-3 gap-6"
          }, [
            React.createElement("div", {
              key: "point-cloud",
              className: "bg-blue-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "point-cloud-title",
                className: "text-lg font-bold text-blue-700 mb-3"
              }, "Point Cloud Processing"),
              React.createElement("ul", {
                key: "point-cloud-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("Statistical Outlier Removal", "pc-1"),
                createListItem("Voxel Downsampling", "pc-2"),
                createListItem("Normal Estimation", "pc-3"),
                createListItem("Background Removal", "pc-4")
              ])
            ]),
            React.createElement("div", {
              key: "mesh-gen",
              className: "bg-purple-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "mesh-title",
                className: "text-lg font-bold text-purple-700 mb-3"
              }, "Mesh Generation"),
              React.createElement("ul", {
                key: "mesh-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("Alpha Shape Computation", "mesh-1"),
                createListItem("Delaunay Triangulation", "mesh-2"),
                createListItem("Topology Verification", "mesh-3"),
                createListItem("Surface Optimization", "mesh-4")
              ])
            ]),
            React.createElement("div", {
              key: "texture",
              className: "bg-green-50 p-6 rounded-lg"
            }, [
              React.createElement("h3", {
                key: "texture-title",
                className: "text-lg font-bold text-green-700 mb-3"
              }, "Texture Mapping"),
              React.createElement("ul", {
                key: "texture-list",
                className: "space-y-2 text-gray-600"
              }, [
                createListItem("UV Coordinate Generation", "texture-1"),
                createListItem("Color Assignment", "texture-2"),
                createListItem("Texture Atlas Creation", "texture-3"),
                createListItem("Quality Enhancement", "texture-4")
              ])
            ])
          ])
        ])
      },
      {
        title: "Results & Performance",
        icon: createIcon(Lucide.BarChart),
        content: React.createElement("div", { className: "space-y-6" }, [
          React.createElement("div", { key: "metrics", className: "grid grid-cols-3 gap-6" }, [
            React.createElement("div", { key: "success", className: "bg-blue-50 p-6 rounded-lg text-center" }, [
              React.createElement("p", { key: "rate", className: "text-3xl font-bold text-blue-600" }, "90%+"),
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-blue-700 mt-2" }, "Success Rate"),
              React.createElement("p", { key: "desc", className: "text-sm text-gray-600 mt-2" }, "Successful model generation from valid scans")
            ]),
            React.createElement("div", { key: "processing", className: "bg-green-50 p-6 rounded-lg text-center" }, [
              React.createElement("p", { key: "time", className: "text-3xl font-bold text-green-600" }, "4-25s"),
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-green-700 mt-2" }, "Processing Time"),
              React.createElement("p", { key: "desc", className: "text-sm text-gray-600 mt-2" }, "Based on input complexity")
            ]),
            React.createElement("div", { key: "noise", className: "bg-purple-50 p-6 rounded-lg text-center" }, [
              React.createElement("p", { key: "rate", className: "text-3xl font-bold text-purple-600" }, "60%"),
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-purple-700 mt-2" }, "Noise Reduction"),
              React.createElement("p", { key: "desc", className: "text-sm text-gray-600 mt-2" }, "Average point cloud optimization")
            ])
          ]),
          React.createElement("div", { key: "details", className: "grid grid-cols-2 gap-6" }, [
            React.createElement("div", { key: "performance", className: "bg-gray-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-gray-700 mb-3" }, "Performance Metrics"),
              React.createElement("ul", { key: "metrics-list", className: "space-y-2" }, [
                React.createElement("li", { key: "small", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Small Files (200K-400K points)"),
                  React.createElement("span", { key: "value", className: "font-bold text-green-600" }, "4s")
                ]),
                React.createElement("li", { key: "medium", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Medium Files (400K-1M points)"),
                  React.createElement("span", { key: "value", className: "font-bold text-blue-600" }, "14s")
                ]),
                React.createElement("li", { key: "large", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Large Files (1M-3M points)"),
                  React.createElement("span", { key: "value", className: "font-bold text-purple-600" }, "25s")
                ])
              ])
            ]),
            React.createElement("div", { key: "quality", className: "bg-gray-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-gray-700 mb-3" }, "Quality Metrics"),
              React.createElement("ul", { key: "quality-list", className: "space-y-2" }, [
                React.createElement("li", { key: "mesh", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Mesh Quality Score"),
                  React.createElement("span", { key: "value", className: "font-bold text-green-600" }, "9.3/10")
                ]),
                React.createElement("li", { key: "texture", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Texture Quality"),
                  React.createElement("span", { key: "value", className: "font-bold text-blue-600" }, "9.5/10")
                ]),
                React.createElement("li", { key: "appearance", className: "flex justify-between items-center" }, [
                  React.createElement("span", { key: "label", className: "text-gray-600" }, "Overall Appearance"),
                  React.createElement("span", { key: "value", className: "font-bold text-purple-600" }, "9.0/10")
                ])
              ])
            ])
          ])
        ])
      },
      {
        title: "Real-World Impact",
        icon: createIcon(Lucide.Target),
        content: React.createElement("div", { className: "space-y-6" }, [
          React.createElement("div", { key: "main-content", className: "grid grid-cols-2 gap-6" }, [
            React.createElement("div", { key: "use-cases", className: "bg-blue-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-blue-700 mb-4" }, "Use Cases"),
              React.createElement("div", { key: "cases", className: "space-y-4" }, [
                React.createElement("div", { key: "case1", className: "bg-white p-4 rounded-lg" }, [
                  React.createElement("h4", { key: "title", className: "font-bold" }, "Product Design"),
                  React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "40% reduction in prototyping time")
                ]),
                React.createElement("div", { key: "case2", className: "bg-white p-4 rounded-lg" }, [
                  React.createElement("h4", { key: "title", className: "font-bold" }, "Cultural Heritage"),
                  React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "Digital preservation of artifacts")
                ]),
                React.createElement("div", { key: "case3", className: "bg-white p-4 rounded-lg" }, [
                  React.createElement("h4", { key: "title", className: "font-bold" }, "Education"),
                  React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "Enhanced 3D learning resources")
                ])
              ])
            ]),
            React.createElement("div", { key: "benefits", className: "bg-green-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-green-700 mb-4" }, "Key Benefits"),
              React.createElement("ul", { key: "benefits-list", className: "space-y-3 text-gray-600" }, [
                createListItem("Cost reduction vs traditional methods", "benefit1"),
                createListItem("Accelerated design processes", "benefit2"),
                createListItem("Improved accessibility to 3D scanning", "benefit3"),
                createListItem("Reduced environmental impact", "benefit4"),
                createListItem("Enhanced collaboration capabilities", "benefit5")
              ])
            ])
          ]),
          React.createElement("div", { key: "achievements", className: "bg-purple-50 p-6 rounded-lg" }, [
            React.createElement("h3", { key: "title", className: "text-lg font-bold text-purple-700 mb-4" }, "Achievements"),
            React.createElement("div", { key: "stats", className: "grid grid-cols-3 gap-4" }, [
              React.createElement("div", { key: "cost", className: "text-center" }, [
                React.createElement("p", { key: "value", className: "text-2xl font-bold text-purple-600" }, "60%"),
                React.createElement("p", { key: "label", className: "text-sm text-gray-600" }, "Cost Reduction")
              ]),
              React.createElement("div", { key: "time", className: "text-center" }, [
                React.createElement("p", { key: "value", className: "text-2xl font-bold text-purple-600" }, "40%"),
                React.createElement("p", { key: "label", className: "text-sm text-gray-600" }, "Time Saved")
              ]),
              React.createElement("div", { key: "satisfaction", className: "text-center" }, [
                React.createElement("p", { key: "value", className: "text-2xl font-bold text-purple-600" }, "90%"),
                React.createElement("p", { key: "label", className: "text-sm text-gray-600" }, "User Satisfaction")
              ])
            ])
          ])
        ])
      },
      {
        title: "System Demo",
        icon: createIcon(Lucide.Monitor),
        content: React.createElement("div", { className: "space-y-6" }, [
          React.createElement("div", { key: "overview", className: "bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg" }, [
            React.createElement("h3", { key: "title", className: "text-xl font-bold mb-4" }, "Demo Overview"),
            React.createElement("div", { key: "steps", className: "grid grid-cols-3 gap-4" }, [
              React.createElement("div", { key: "input", className: "bg-white p-4 rounded-lg text-center" }, [
                React.createElement("p", { key: "title", className: "font-bold text-blue-600" }, "Input"),
                React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "LIDAR Scan Data")
              ]),
              React.createElement("div", { key: "processing", className: "bg-white p-4 rounded-lg text-center" }, [
                React.createElement("p", { key: "title", className: "font-bold text-purple-600" }, "Processing"),
                React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "Real-time Pipeline")
              ]),
              React.createElement("div", { key: "output", className: "bg-white p-4 rounded-lg text-center" }, [
                React.createElement("p", { key: "title", className: "font-bold text-green-600" }, "Output"),
                React.createElement("p", { key: "desc", className: "text-sm text-gray-600" }, "3D Model Generation")
              ])
            ])
          ]),
          React.createElement("div", { key: "details", className: "grid grid-cols-2 gap-6" }, [
            React.createElement("div", { key: "features", className: "bg-gray-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-gray-700 mb-3" }, "Key Features Demo"),
              React.createElement("ul", { key: "feature-list", className: "space-y-2" }, [
                createListItem("File upload and processing", "feature1"),
                createListItem("Real-time progress tracking", "feature2"),
                createListItem("Interactive 3D visualization", "feature3"),
                createListItem("Export functionality", "feature4")
              ])
            ]),
            React.createElement("div", { key: "objects", className: "bg-gray-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-gray-700 mb-3" }, "Demo Objects"),
              React.createElement("ul", { key: "object-list", className: "space-y-2" }, [
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
        content: React.createElement("div", { className: "space-y-6" }, [
          React.createElement("div", { key: "goals", className: "grid grid-cols-2 gap-6" }, [
            React.createElement("div", { key: "short-term", className: "bg-blue-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-blue-700 mb-3" }, "Short-term Goals"),
              React.createElement("ul", { key: "goal-list", className: "space-y-2" }, [
                createListItem("Cloud integration (AWS)", "goal1"),
                createListItem("Mobile application development", "goal2"),
                createListItem("Enhanced preprocessing algorithms", "goal3"),
                createListItem("Advanced texture mapping", "goal4")
              ])
            ]),
            React.createElement("div", { key: "long-term", className: "bg-purple-50 p-6 rounded-lg" }, [
              React.createElement("h3", { key: "title", className: "text-lg font-bold text-purple-700 mb-3" }, "Long-term Vision"),
              React.createElement("ul", { key: "vision-list", className: "space-y-2" }, [
                createListItem("AI-powered optimization", "vision1"),
                createListItem("Real-time reconstruction", "vision2"),
                createListItem("Multi-object scanning", "vision3"),
                createListItem("Industry-standard integration", "vision4")
              ])
            ])
          ]),
          React.createElement("div", { key: "research", className: "bg-green-50 p-6 rounded-lg" }, [
            React.createElement("h3", { key: "title", className: "text-lg font-bold text-green-700 mb-3" }, "Research Directions"),
            React.createElement("div", { key: "directions", className: "grid grid-cols-2 gap-4" }, [
              React.createElement("ul", { key: "list1", className: "space-y-2" }, [
                createListItem("Advanced ML algorithms", "research1"),
                createListItem("Environmental modeling", "research2"),
                createListItem("Automated parameter tuning", "research3")
              ]),
              React.createElement("ul", { key: "list2", className: "space-y-2" }, [
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
        content: React.createElement("div", { className: "space-y-6 text-center" }, [
          React.createElement("h2", { key: "title", className: "text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text" }, "Ready for Questions"),
          React.createElement("p", { key: "subtitle", className: "text-xl text-gray-600" }, "Thank you for your attention"),
          React.createElement("div", { key: "project", className: "mt-8" }, [
            React.createElement("div", { key: "info", className: "bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg" }, [
              React.createElement("p", { key: "name", className: "text-lg text-gray-700" }, "DroMo Project"),
              React.createElement("p", { key: "tagline", className: "text-gray-600" }, "Transforming Reality into Digital 3D")
            ])
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

    // Add keyboard and click controls
    useEffect(() => {
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

        const handleClick = (e) => {
          if (!isFullscreen) return;

          // Left click advances, right click goes back
          if (e.button === 0) { // Left click
            nextSlide();
          } else if (e.button === 2) { // Right click
            e.preventDefault();
            previousSlide();
          }
        };

        const handleContextMenu = (e) => {
          if (isFullscreen) {
            e.preventDefault();
          }
        };

        // Add keyboard listener to the specific tab content element to avoid conflicts
        const aboutUsTab = document.getElementById('AboutUsTab');
        if (aboutUsTab) {
        aboutUsTab.addEventListener('keydown', handleKeyPress);
        } else {
        document.addEventListener('keydown', handleKeyPress);
        }
        // document.addEventListener('keydown', handleKeyPress);
        document.addEventListener('mouseup', handleClick);
        document.addEventListener('contextmenu', handleContextMenu);

        return () => {
        //   document.removeEventListener('keydown', handleKeyPress);
          if (aboutUsTab) {
            aboutUsTab.removeEventListener('keydown', handleKeyPress);
          } else {
            document.removeEventListener('keydown', handleKeyPress);
          }
          document.removeEventListener('mouseup', handleClick);
          document.removeEventListener('contextmenu', handleContextMenu);
        };
      }, [isFullscreen, currentSlide]); // Dependencies array

      // Toggle fullscreen
      const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
      };
      return React.createElement("div", {
        className: `${isFullscreen ? 'fixed inset-0 bg-gray-50 z-50' : 'min-h-screen bg-gray-50'} p-8`,
        tabIndex: "0",
      },
        React.createElement("div", {
          className: `${isFullscreen ? 'h-full' : 'max-w-7xl mx-auto'} bg-white rounded-xl shadow-lg p-8 relative`
        }, [
          // Fullscreen toggle button remains the same...
          React.createElement("button", {
            key: "fullscreen",
            onClick: toggleFullscreen,
            className: "absolute top-4 right-4 p-2 text-gray-600 hover:text-gray-900",
            title: isFullscreen ? "Exit Fullscreen" : "Enter Fullscreen"
          },
            React.createElement(isFullscreen ? Lucide.Minimize2 : Lucide.Maximize2, {
              size: 24
            })
          ),
          // Add fixed height container for slide content
          React.createElement("div", {
            key: "slide-container",
            className: "flex flex-col h-[800px]" // Fixed height container
          }, [
            // Header
            React.createElement("div", {
              key: "header",
              className: "flex items-center space-x-4 mb-6"
            }, [
              slides[currentSlide].icon,
              React.createElement("h1", {
                className: "text-3xl font-bold text-gray-800"
              }, slides[currentSlide].title)
            ]),
            // Content with overflow handling
            React.createElement("div", {
              key: "content",
              className: `flex-1 overflow-auto mb-8 ${isFullscreen ? 'text-lg' : ''}`
            }, slides[currentSlide].content),
            // Navigation
            React.createElement("div", {
              key: "navigation",
              className: "flex justify-between items-center mt-auto pt-4" // Changed to mt-auto to stick to bottom
            }, [
              React.createElement("button", {
                key: "prev",
                onClick: previousSlide,
                className: `px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-md hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center ${isFullscreen ? 'opacity-0 hover:opacity-100' : ''}`,
                disabled: currentSlide === 0
              }, [
                React.createElement(Lucide.ChevronLeft, {
                  key: "icon",
                  className: "mr-2",
                  size: 20
                }),
                "Previous"
              ]),
              React.createElement("span", {
                key: "counter",
                className: "text-gray-600 font-medium"
              }, `${currentSlide + 1} / ${slides.length}`),
              React.createElement("button", {
                key: "next",
                onClick: nextSlide,
                className: `px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg shadow-md hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center ${isFullscreen ? 'opacity-0 hover:opacity-100' : ''}`,
                disabled: currentSlide === slides.length - 1
              }, [
                "Next",
                React.createElement(Lucide.ChevronRight, {
                  key: "icon",
                  className: "ml-2",
                  size: 20
                })
              ])
            ])
          ]),

          // Only show controls hint in fullscreen mode
          isFullscreen && React.createElement("div", {
            key: "controls-hint",
            className: "absolute bottom-4 left-1/2 transform -translate-x-1/2 text-gray-500 text-sm opacity-50"
          }, "Use arrow keys or space to navigate"),
          // Add a smaller hint for non-fullscreen mode
          !isFullscreen && React.createElement("div", {
            key: "controls-hint-mini",
            className: "absolute bottom-2 left-1/2 transform -translate-x-1/2 text-gray-400 text-xs"
          }, "Use space or mouse clicks to navigate")
        ])
      );
    };

    export default AboutUs;

import { useEffect, useState } from "react";
import axios from "axios";
import {
  Wind,
  Activity,
  MapPin,
  TrendingUp,
  AlertTriangle,
  Leaf,
  Factory,
  Database,
  Brain,
  CloudRain,
  Car,
  CalendarDays,
  BarChart3,
  Cpu,
  Layers,
  ArrowUpRight
} from "lucide-react";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup
} from "react-leaflet";

import "leaflet/dist/leaflet.css";
import "./App.css";

const API = "http://localhost:8000";

const cityCoordinates = {
  Ahmedabad: [23.0225, 72.5714],
  Aizawl: [23.7271, 92.7176],
  Amaravati: [16.5062, 80.648],
  Amritsar: [31.634, 74.8723],
  Bengaluru: [12.9716, 77.5946],
  Bhopal: [23.2599, 77.4126],
  Brajrajnagar: [21.8167, 83.9167],
  Chandigarh: [30.7333, 76.7794],
  Chennai: [13.0827, 80.2707],
  Coimbatore: [11.0168, 76.9558],
  Delhi: [28.6139, 77.209],
  Ernakulam: [9.9816, 76.2999],
  Guwahati: [26.1445, 91.7362],
  Gurugram: [28.4595, 77.0266],
  Hyderabad: [17.385, 78.4867],
  Jaipur: [26.9124, 75.7873],
  Jorapokhar: [23.7167, 86.4167],
  Kochi: [9.9312, 76.2673],
  Kolkata: [22.5726, 88.3639],
  Lucknow: [26.8467, 80.9462],
  Mumbai: [19.076, 72.8777],
  Patna: [25.5941, 85.1376],
  Shillong: [25.5788, 91.8933],
  Talcher: [20.9517, 85.2167],
  Thiruvananthapuram: [8.5241, 76.9366],
  Visakhapatnam: [17.6868, 83.2185]
};

function getAQIColor(aqi) {
  if (aqi <= 50) return "#35d07f";
  if (aqi <= 100) return "#9be15d";
  if (aqi <= 200) return "#f5d547";
  if (aqi <= 300) return "#ff9f43";
  if (aqi <= 400) return "#ff5c5c";
  return "#c83bff";
}

function getAQILabel(aqi) {
  if (aqi <= 50) return "Good";
  if (aqi <= 100) return "Satisfactory";
  if (aqi <= 200) return "Moderate";
  if (aqi <= 300) return "Poor";
  if (aqi <= 400) return "Very Poor";
  return "Severe";
}

function App() {
  const [overview, setOverview] = useState(null);
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState("");
  const [cityData, setCityData] = useState(null);
  const [timeline, setTimeline] = useState([]);
  const [topCities, setTopCities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboard();
  }, []);

  useEffect(() => {
    if (selectedCity) {
      loadCity(selectedCity);
    }
  }, [selectedCity]);

  async function loadDashboard() {
    try {
      setError("");

      const [
        overviewResponse,
        citiesResponse,
        topResponse
      ] = await Promise.all([
        axios.get(`${API}/overview`),
        axios.get(`${API}/cities`),
        axios.get(`${API}/top-polluted`)
      ]);

      setOverview(overviewResponse.data);

      const cityList = citiesResponse.data.cities || [];

      setCities(cityList);
      setTopCities(topResponse.data.cities || []);

      if (cityList.length > 0) {
        setSelectedCity(cityList[0].city);
      }
    } catch (err) {
      console.error("Dashboard loading failed:", err);
      setError("Unable to connect to the AERIS backend.");
    } finally {
      setLoading(false);
    }
  }

  async function loadCity(city) {
    try {
      const [cityResponse, timelineResponse] = await Promise.all([
        axios.get(`${API}/city/${encodeURIComponent(city)}`),
        axios.get(`${API}/timeline/${encodeURIComponent(city)}`)
      ]);

      setCityData(cityResponse.data);
      setTimeline(timelineResponse.data.data || []);
    } catch (err) {
      console.error("City loading failed:", err);
    }
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-orb">
          <Wind size={25} />
        </div>
        <h2>AERIS</h2>
        <p>Reading atmospheric intelligence...</p>
      </div>
    );
  }

  return (
    <div className="app">

      <div className="ambient ambient-one" />
      <div className="ambient ambient-two" />

      {/* NAVBAR */}

      <nav className="navbar">

        <div className="brand">
          <div className="brand-icon">
            <Wind size={22} />
          </div>

          <div>
            <h1>AERIS</h1>
            <span>Atmospheric Intelligence System</span>
          </div>
        </div>

        <div className="nav-links">
          <a href="#overview">Overview</a>
          <a href="#historical">Historical AQI</a>
          <a href="#ml">ML Intelligence</a>
          <a href="#pipeline">Pipeline</a>
        </div>

        <div className="system-status">
          <span className="status-dot" />
          SYSTEM ONLINE
        </div>

      </nav>


      {/* HERO */}

      <section className="hero" id="overview">

        <div className="hero-content">

          <div className="eyebrow">
            <Leaf size={15} />
            INDIA • AIR • DATA • INTELLIGENCE
          </div>

          <h2>
            Reading the
            <span> breath of India.</span>
          </h2>

          <p className="hero-description">
            AERIS transforms large-scale air-quality observations into
            environmental intelligence using distributed data processing,
            machine learning and interactive visual analytics.
          </p>

          <div className="hero-actions">
            <a href="#historical" className="primary-action">
              Explore intelligence
              <ArrowUpRight size={17} />
            </a>

            <div className="hero-status">
              <span />
              26 monitored cities
            </div>
          </div>

        </div>

        <div className="hero-orbit">

          <div className="orbit-ring ring-one" />
          <div className="orbit-ring ring-two" />

          <div className="orbit-particle particle-one" />
          <div className="orbit-particle particle-two" />

          <div className="air-core">
            <Wind size={36} />
            <strong>AIR</strong>
            <span>INTELLIGENCE</span>
          </div>

        </div>

      </section>


      {/* PROJECT OVERVIEW */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">PROJECT OVERVIEW</span>
            <h2>Environmental intelligence at scale</h2>
          </div>

          <Database size={21} />

        </div>

        <div className="overview-grid">

          <div className="overview-card overview-main">
            <div className="overview-icon">
              <Layers size={24} />
            </div>

            <h3>From raw observations to insight</h3>

            <p>
              AERIS combines historical air-quality observations,
              distributed processing with Hadoop and Spark, and a
              Random Forest regression model to analyse and predict
              atmospheric conditions across Indian cities.
            </p>

            <div className="overview-tags">
              <span>HADOOP</span>
              <span>SPARK</span>
              <span>MACHINE LEARNING</span>
              <span>FASTAPI</span>
              <span>REACT</span>
            </div>
          </div>

          <div className="overview-mini">
            <Activity size={21} />
            <strong>{overview?.records?.toLocaleString() || "24,850"}</strong>
            <span>observations processed</span>
          </div>

          <div className="overview-mini">
            <MapPin size={21} />
            <strong>{cities.length}</strong>
            <span>Indian cities monitored</span>
          </div>

          <div className="overview-mini">
            <Brain size={21} />
            <strong>83.1%</strong>
            <span>model R² score</span>
          </div>

        </div>

      </section>


      {/* KPI SECTION */}

      <section className="metrics">

        <div className="metric-card">
          <div className="metric-icon">
            <Activity size={20} />
          </div>

          <div className="metric-content">
            <span>Total observations</span>
            <strong>
              {overview?.records?.toLocaleString() || "--"}
            </strong>
            <small>Historical records processed</small>
          </div>

          <ArrowUpRight className="metric-arrow" size={17} />
        </div>


        <div className="metric-card">
          <div className="metric-icon">
            <MapPin size={20} />
          </div>

          <div className="metric-content">
            <span>Cities monitored</span>
            <strong>{cities.length}</strong>
            <small>Across India</small>
          </div>

          <ArrowUpRight className="metric-arrow" size={17} />
        </div>


        <div className="metric-card">
          <div className="metric-icon">
            <Wind size={20} />
          </div>

          <div className="metric-content">
            <span>Average AQI</span>
            <strong>{overview?.average_aqi}</strong>
            <small>Historical average</small>
          </div>

          <ArrowUpRight className="metric-arrow" size={17} />
        </div>


        <div className="metric-card">
          <div className="metric-icon warning">
            <AlertTriangle size={20} />
          </div>

          <div className="metric-content">
            <span>Peak AQI recorded</span>
            <strong>{overview?.maximum_aqi}</strong>
            <small>Maximum observation</small>
          </div>

          <ArrowUpRight className="metric-arrow" size={17} />
        </div>

      </section>


      {/* HISTORICAL AQI */}

      <section className="section-shell" id="historical">

        <div className="section-heading">

          <div>
            <span className="section-label">HISTORICAL AQI</span>
            <h2>India's pollution landscape</h2>
          </div>

          <BarChart3 size={21} />

        </div>

        <div className="map-card">

          <div className="map-topbar">

            <div>
              <span>LIVE DATA VIEW</span>
              <strong>Average AQI across monitored cities</strong>
            </div>

            <div className="map-summary">
              <Wind size={16} />
              Historical observations
            </div>

          </div>

          <div className="map-wrapper">

            <MapContainer
              center={[22.5, 79]}
              zoom={4.7}
              scrollWheelZoom={true}
              className="india-map"
            >

              <TileLayer
                attribution="&copy; OpenStreetMap contributors"
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />

              {cities.map((city) => {

                const coordinates = cityCoordinates[city.city];

                if (!coordinates) {
                  return null;
                }

                const color = getAQIColor(city.average_aqi);
                const selected = city.city === selectedCity;

                return (
                  <CircleMarker
                    key={city.city}
                    center={coordinates}
                    radius={selected ? 13 : 8}
                    pathOptions={{
                      color: "#ffffff",
                      fillColor: color,
                      fillOpacity: 0.85,
                      weight: selected ? 3 : 1
                    }}
                    eventHandlers={{
                      click: () => setSelectedCity(city.city)
                    }}
                  >

                    <Popup>

                      <div className="popup">
                        <h4>{city.city}</h4>

                        <div>
                          AQI:
                          <strong> {city.average_aqi}</strong>
                        </div>

                        <div>
                          Predicted:
                          <strong> {city.average_predicted_aqi}</strong>
                        </div>

                        <div>
                          Maximum:
                          <strong> {city.maximum_aqi}</strong>
                        </div>

                        <div>
                          Records:
                          <strong> {city.records}</strong>
                        </div>
                      </div>

                    </Popup>

                  </CircleMarker>
                );
              })}

            </MapContainer>

            <div className="map-overlay">
              <span>INDIA</span>
              <strong>{cities.length}</strong>
              <small>MONITORED CITIES</small>
            </div>

          </div>

          <div className="map-legend">

            <span>
              <i className="legend-dot good" />
              Good
            </span>

            <span>
              <i className="legend-dot moderate" />
              Moderate
            </span>

            <span>
              <i className="legend-dot poor" />
              Poor
            </span>

            <span>
              <i className="legend-dot severe" />
              Severe
            </span>

          </div>

        </div>

      </section>


      {/* CITY INTELLIGENCE */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">CITY INTELLIGENCE</span>
            <h2>Explore atmospheric conditions</h2>
          </div>

          <MapPin size={21} />

        </div>

        <div className="city-panel">

          <div className="city-toolbar">

            <div>
              <span>SELECTED REGION</span>
              <h3>{selectedCity || "Select a city"}</h3>
            </div>

            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
            >

              {cities.map((city) => (
                <option
                  key={city.city}
                  value={city.city}
                >
                  {city.city}
                </option>
              ))}

            </select>

          </div>


          {cityData && (

            <>

              <div className="city-main">

                <div>
                  <span className="city-label">AVERAGE AQI</span>

                  <div className="city-aqi-number">
                    {cityData.average_aqi}
                  </div>

                  <div
                    className="aqi-status"
                    style={{
                      color: getAQIColor(cityData.average_aqi)
                    }}
                  >
                    <span
                      style={{
                        background: getAQIColor(cityData.average_aqi)
                      }}
                    />
                    {getAQILabel(cityData.average_aqi)}
                  </div>
                </div>

                <div className="city-description">
                  <p>
                    Historical atmospheric observations for{" "}
                    <strong>{cityData.city}</strong>, compared
                    with the machine-learning prediction generated
                    by the AERIS pipeline.
                  </p>
                </div>

              </div>


              <div className="city-metrics">

                <div>
                  <span>Predicted AQI</span>
                  <strong>{cityData.average_predicted_aqi}</strong>
                </div>

                <div>
                  <span>Maximum</span>
                  <strong>{cityData.maximum_aqi}</strong>
                </div>

                <div>
                  <span>Minimum</span>
                  <strong>{cityData.minimum_aqi}</strong>
                </div>

                <div>
                  <span>Records</span>
                  <strong>{cityData.records}</strong>
                </div>

              </div>


              <div className="comparison">

                <div>
                  <span>OBSERVED AQI</span>

                  <div className="bar">
                    <div
                      style={{
                        width: `${Math.min(
                          cityData.average_aqi / 5,
                          100
                        )}%`
                      }}
                    />
                  </div>
                </div>

                <div>
                  <span>ML PREDICTED AQI</span>

                  <div className="bar predicted">
                    <div
                      style={{
                        width: `${Math.min(
                          cityData.average_predicted_aqi / 5,
                          100
                        )}%`
                      }}
                    />
                  </div>
                </div>

              </div>

            </>

          )}

        </div>

      </section>


      {/* HISTORICAL TIMELINE */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">TEMPORAL ANALYSIS</span>
            <h2>Historical AQI trajectory</h2>
          </div>

          <CalendarDays size={21} />

        </div>

        <div className="timeline-panel">

          <div className="timeline-header">
            <div>
              <span>{selectedCity}</span>
              <strong>Observed vs predicted behaviour</strong>
            </div>

            <div className="timeline-legend">
              <span>
                <i className="observed-dot" />
                Observed
              </span>

              <span>
                <i className="predicted-dot" />
                Predicted
              </span>
            </div>
          </div>


          <div className="timeline">

            {timeline.length > 0 ? (

              timeline.slice(-18).map((item, index) => {

                const height = Math.min(
                  Math.max((item.aqi || 0) / 5, 8),
                  100
                );

                const predictedHeight = Math.min(
                  Math.max((item.predicted_aqi || 0) / 5, 8),
                  100
                );

                return (
                  <div className="timeline-column" key={`${item.date}-${index}`}>

                    <div className="timeline-bars">

                      <div
                        className="timeline-bar observed"
                        style={{ height: `${height}%` }}
                      />

                      <div
                        className="timeline-bar predicted"
                        style={{ height: `${predictedHeight}%` }}
                      />

                    </div>

                    <span>
                      {String(item.date).slice(5, 10)}
                    </span>

                  </div>
                );

              })

            ) : (

              <div className="empty-state">
                Historical timeline unavailable.
              </div>

            )}

          </div>

        </div>

      </section>


      {/* POLLUTION HOTSPOTS */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">POLLUTION HOTSPOTS</span>
            <h2>Where atmospheric pressure is highest</h2>
          </div>

          <Factory size={21} />

        </div>

        <div className="hotspot-grid">

          <div className="hotspot-panel">

            {topCities.map((city, index) => {

              const width = Math.min(
                (city.average_aqi / 500) * 100,
                100
              );

              return (
                <div
                  className="hotspot"
                  key={city.city}
                  onClick={() => setSelectedCity(city.city)}
                >

                  <div className="hotspot-number">
                    {String(index + 1).padStart(2, "0")}
                  </div>

                  <div className="hotspot-info">

                    <div className="hotspot-name">
                      <span>{city.city}</span>
                      <strong>{city.average_aqi}</strong>
                    </div>

                    <div className="bar">
                      <div
                        className="bar-fill"
                        style={{
                          width: `${width}%`,
                          background: getAQIColor(
                            city.average_aqi
                          )
                        }}
                      />
                    </div>

                  </div>

                </div>
              );

            })}

          </div>

          <div className="hotspot-insight">

            <div className="insight-icon">
              <AlertTriangle size={25} />
            </div>

            <span>ATMOSPHERIC SIGNAL</span>

            <h3>
              Pollution patterns vary substantially
              between Indian regions.
            </h3>

            <p>
              AERIS aggregates observations across cities to
              reveal geographic differences in air-quality
              conditions and identify locations requiring
              closer attention.
            </p>

          </div>

        </div>

      </section>


      {/* ML PREDICTIONS */}

      <section className="section-shell" id="ml">

        <div className="section-heading">

          <div>
            <span className="section-label">MACHINE LEARNING</span>
            <h2>Predictive atmosphere</h2>
          </div>

          <Brain size={21} />

        </div>

        <div className="ml-grid">

          <div className="ml-main">

            <div className="ml-ring">

              <div>
                <strong>83.1%</strong>
                <span>R² SCORE</span>
              </div>

            </div>

            <div className="ml-copy">

              <span>MODEL ENGINE</span>

              <h3>Random Forest Regression</h3>

              <p>
                The model learns relationships within historical
                atmospheric observations and estimates AQI behaviour
                from the learned patterns.
              </p>

            </div>

          </div>


          <div className="ml-stat">

            <TrendingUp size={21} />

            <span>R² SCORE</span>
            <strong>0.8309</strong>

          </div>


          <div className="ml-stat">

            <Activity size={21} />

            <span>RMSE</span>
            <strong>60.62</strong>

          </div>


          <div className="ml-stat">

            <BarChart3 size={21} />

            <span>MAE</span>
            <strong>32.04</strong>

          </div>


          <div className="ml-stat">

            <Database size={21} />

            <span>PREDICTIONS</span>
            <strong>24,850</strong>

          </div>

        </div>

      </section>


      {/* 2026 FORECAST */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">2026 FORECAST</span>
            <h2>Future atmospheric intelligence</h2>
          </div>

          <TrendingUp size={21} />

        </div>

        <div className="future-card">

          <div className="future-icon">
            <CalendarDays size={28} />
          </div>

          <div>
            <span>FORECAST MODULE</span>

            <h3>2026 AQI forecasting layer</h3>

            <p>
              The AERIS architecture is prepared to incorporate
              future AQI forecasts generated from the trained
              machine-learning pipeline.
            </p>
          </div>

          <div className="module-status">
            <span />
            DATA MODULE
            <strong>READY FOR INTEGRATION</strong>
          </div>

        </div>

      </section>


      {/* WEATHER + VEHICLE */}

      <section className="section-shell">

        <div className="section-heading">

          <div>
            <span className="section-label">ENVIRONMENTAL FACTORS</span>
            <h2>Beyond AQI</h2>
          </div>

          <CloudRain size={21} />

        </div>

        <div className="factor-grid">

          <div className="factor-card weather-card">

            <div className="factor-icon">
              <CloudRain size={25} />
            </div>

            <span>WEATHER ANALYSIS</span>

            <h3>Atmosphere meets weather</h3>

            <p>
              Future integration of temperature, humidity,
              wind, rainfall and atmospheric conditions can
              provide additional context for AQI behaviour.
            </p>

            <div className="module-pill">
              <span />
              WEATHER DATA LAYER
            </div>

          </div>


          <div className="factor-card vehicle-card">

            <div className="factor-icon">
              <Car size={25} />
            </div>

            <span>VEHICLE ANALYSIS</span>

            <h3>Understanding mobility pressure</h3>

            <p>
              Vehicle-density and transport-emission data can
              be incorporated to study the relationship between
              urban mobility and air-quality conditions.
            </p>

            <div className="module-pill">
              <span />
              VEHICLE DATA LAYER
            </div>

          </div>

        </div>

      </section>


      {/* BIG DATA PIPELINE */}

      <section className="section-shell" id="pipeline">

        <div className="section-heading">

          <div>
            <span className="section-label">BIG DATA PIPELINE</span>
            <h2>From distributed data to intelligence</h2>
          </div>

          <Cpu size={21} />

        </div>

        <div className="pipeline">

          <div className="pipeline-step">
            <div className="pipeline-number">01</div>
            <Database size={23} />
            <span>INGESTION</span>
            <strong>Air Quality Data</strong>
            <p>Historical observations enter the processing pipeline.</p>
          </div>

          <div className="pipeline-line" />

          <div className="pipeline-step">
            <div className="pipeline-number">02</div>
            <Layers size={23} />
            <span>DISTRIBUTED STORAGE</span>
            <strong>HDFS</strong>
            <p>Large datasets are distributed across the Hadoop ecosystem.</p>
          </div>

          <div className="pipeline-line" />

          <div className="pipeline-step">
            <div className="pipeline-number">03</div>
            <Cpu size={23} />
            <span>PROCESSING</span>
            <strong>Apache Spark</strong>
            <p>Distributed computation transforms raw observations.</p>
          </div>

          <div className="pipeline-line" />

          <div className="pipeline-step">
            <div className="pipeline-number">04</div>
            <Brain size={23} />
            <span>INTELLIGENCE</span>
            <strong>Random Forest</strong>
            <p>Machine learning generates AQI predictions.</p>
          </div>

          <div className="pipeline-line" />

          <div className="pipeline-step">
            <div className="pipeline-number">05</div>
            <Activity size={23} />
            <span>DELIVERY</span>
            <strong>AERIS API</strong>
            <p>FastAPI exposes environmental intelligence to the dashboard.</p>
          </div>

        </div>

      </section>


      {/* FOOTER */}

      <footer>

        <div>
          <Leaf size={16} />
          AERIS • Environmental Intelligence
        </div>

        <span>
          Hadoop • Spark • Machine Learning • FastAPI • React
        </span>

      </footer>

    </div>
  );
}

export default App;


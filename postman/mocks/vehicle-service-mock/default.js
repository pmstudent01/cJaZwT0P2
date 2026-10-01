/**
 * Mock server for Vehicle Service Collection
 *
 * Endpoints:
 *   1. POST   /vehicles         - Create a vehicle
 *   2. GET    /vehicles         - Get all vehicles
 *   3. GET    /vehicles/:id     - Retrieve a vehicle
 *   4. PATCH  /vehicles/:id     - Update a vehicle
 *   5. DELETE /vehicles/:id     - Delete a vehicle
 *
 * Click Start to run the mock locally.
 * Deploying gives you a shareable URL for CI and team use.
 */
const http = require("http");
const PORT = process.env.PORT || 4500;
const JSON_HEADER = { "Content-Type": "application/json" };

const server = http.createServer(async (req, res) => {
  const { method, url } = req;

  // Helper: parse request body as JSON
  const parseBody = () =>
    new Promise((resolve) => {
      let raw = "";
      req.on("data", (c) => (raw += c));
      req.on("end", () => {
        try { resolve(raw ? JSON.parse(raw) : {}); } catch { resolve({}); }
      });
    });

  // Helper: extract :id from /vehicles/:id
  const vehicleIdMatch = url.match(/^\/vehicles\/([^/?]+)/);
  const vehicleId = vehicleIdMatch ? vehicleIdMatch[1] : null;

  // @endpoint POST /vehicles
  if (method === "POST" && url === "/vehicles") {
    return pm.mock.matchRequest(
      "postman/collections/Vehicle Service Collection/Create a vehicle.request.yaml",
      req
    )
      ? pm.mock.sendExample(
          "postman/collections/Vehicle Service Collection/.resources/Create a vehicle.resources/examples/201 - Success.example.yaml",
          res
        )
      : (() => {
          res.writeHead(201, JSON_HEADER);
          return res.end(
            JSON.stringify({
              id: Date.now(),
              nickName: "The Lisa Marie",
              vin: "4M2DV11W4RDJ53329",
              make: "Mercury",
              model: "Villager",
              year: "1994",
              miles: 159864,
            })
          );
        })();
  }

  // @endpoint GET /vehicles
  if (method === "GET" && url === "/vehicles") {
    return pm.mock.matchRequest(
      "postman/collections/Vehicle Service Collection/Get all vehicles.request.yaml",
      req
    )
      ? pm.mock.sendExample(
          "postman/collections/Vehicle Service Collection/.resources/Get all vehicles.resources/examples/200 - Success.example.yaml",
          res
        )
      : (() => {
          res.writeHead(200, JSON_HEADER);
          return res.end(
            JSON.stringify({
              vehicles: [
                {
                  id: 1,
                  nickName: "The Lisa Marie",
                  vin: "4M2DV11W4RDJ53329",
                  make: "Mercury",
                  model: "Villager",
                  year: "1994",
                  miles: 159864,
                },
              ],
            })
          );
        })();
  }

  // @endpoint GET /vehicles/:id
  if (method === "GET" && vehicleId) {
    return pm.mock.matchRequest(
      "postman/collections/Vehicle Service Collection/Retrieve a vehicle.request.yaml",
      req
    )
      ? pm.mock.sendExample(
          "postman/collections/Vehicle Service Collection/.resources/Retrieve a vehicle.resources/examples/200 - Success.example.yaml",
          res
        )
      : (() => {
          res.writeHead(200, JSON_HEADER);
          return res.end(
            JSON.stringify({
              id: vehicleId,
              nickName: "The Lisa Marie",
              vin: "4M2DV11W4RDJ53329",
              make: "Mercury",
              model: "Villager",
              year: "1994",
              miles: 159864,
            })
          );
        })();
  }

  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && vehicleId) {
    return pm.mock.matchRequest(
      "postman/collections/Vehicle Service Collection/Update a collection.request.yaml",
      req
    )
      ? pm.mock.sendExample(
          "postman/collections/Vehicle Service Collection/.resources/Update a collection.resources/examples/200 - Success.example.yaml",
          res
        )
      : (() => {
          res.writeHead(200, JSON_HEADER);
          return res.end(
            JSON.stringify({
              id: vehicleId,
              nickName: "The Lisa Marie",
              vin: "4M2DV11W4RDJ53329",
              make: "Mercury",
              model: "Villager",
              year: "1994",
              miles: 159999,
            })
          );
        })();
  }

  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && vehicleId) {
    return pm.mock.matchRequest(
      "postman/collections/Vehicle Service Collection/Delete a vehicle.request.yaml",
      req
    )
      ? pm.mock.sendExample(
          "postman/collections/Vehicle Service Collection/.resources/Delete a vehicle.resources/examples/204 - Success.example.yaml",
          res
        )
      : (() => {
          res.writeHead(204, JSON_HEADER);
          return res.end();
        })();
  }

  // 404 fallback
  res.writeHead(404, JSON_HEADER);
  res.end(
    JSON.stringify({
      error: "Endpoint not defined",
      message: `No handler for ${method} ${url}`,
    })
  );
});

server.listen(PORT, () => console.log(`Vehicle Service mock running on port ${PORT}`));

const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();

// Promisify Redis methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Array of products
const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

// Data access function
const getItemById = (id) =>
  listProducts.find((product) => product.itemId === id);

// Reserve stock in Redis
const reserveStockById = async (itemId, stock) => {
  await setAsync(`item.${itemId}`, stock);
};

// Get current reserved stock from Redis
const getCurrentReservedStockById = async (itemId) => {
  const reservedStock = await getAsync(`item.${itemId}`);
  return reservedStock ? parseInt(reservedStock) : 0;
};

// Middleware for JSON responses
app.use(express.json());

// Route to list all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Route to get product details by itemId
app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(parseInt(itemId));
  if (product) {
    const currentQuantity = await getCurrentReservedStockById(parseInt(itemId));
    res.json({ ...product, currentQuantity });
  } else {
    res.status(404).json({ status: 'Product not found' });
  }
});

// Route to reserve product by itemId
app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(parseInt(itemId));
  if (!product) {
    res.status(404).json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(parseInt(itemId));
    if (currentQuantity <= 0) {
      res.json({
        status: 'Not enough stock available',
        itemId: product.itemId,
      });
    } else {
      await reserveStockById(parseInt(itemId), currentQuantity - 1);
      res.json({ status: 'Reservation confirmed', itemId: product.itemId });
    }
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

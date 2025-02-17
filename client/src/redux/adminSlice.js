import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { API_ENDPOINTS } from "../config";
import { getCookie } from "../assets/utils/toolkit";
const token = getCookie("token");
console.log("Token:", token);

if (!token) {
  console.error("Token is missing. Please log in again.");
}

const headers = {
  "Content-Type": "application/json",
  Authorization: token,
};

const initialState = {
  products: { data: [], status: "idle", error: null },
  customers: { data: [], status: "idle", error: null },
  orders: { data: [], status: "idle", error: null },
  tags: { data: [], status: "idle", error: null },
  categories: { data: [], status: "idle", error: null },
  subcategories: { data: [], status: "idle", error: null },
  brands: { data: [], status: "idle", error: null },
  customerOrders: { data: [], status: "idle", error: null },
  customersCount: { data: 0, status: "idle", error: null },
  productsCount: { data: 0, status: "idle", error: null },
  ordersCount: {
    data: 0,
    status: "idle",
    error: null,
  },
  categoriesCount: {
    data: 0,
    status: "idle",
    error: null,
  },
  revenue: {
    data: 0,
    status: "idle",
    error: null,
  },
};

export const fetchCustomerCount = createAsyncThunk(
  "admin/fetchCustomerCount",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CUSTOMERS_COUNT, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch customer count");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchStockCount = createAsyncThunk(
  "admin/fetchStockCount",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.PRODUCTS_COUNT, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch stock count");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const updateOrderStatus = createAsyncThunk(
  "admin/updateOrderStatus",
  async ({ orderId, isFulfilled }, { rejectWithValue }) => {
    try {
      const response = await fetch(
        `${API_ENDPOINTS.ORDERS}/${orderId}/fulfill`,
        {
          method: "PUT",
          headers: headers,
          body: JSON.stringify({ isFulfilled }),
        }
      );

      // Check if the response is successful
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to update order status");
      }

      // Return the response data if the request was successful
      return await response.json();
    } catch (error) {
      // Return the error message if something goes wrong
      return rejectWithValue(error.message);
    }
  }
);

export const fetchRevenue = createAsyncThunk(
  "admin/fetchRevenue",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.REVENUE, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch revenue");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchCategoryCount = createAsyncThunk(
  "admin/fetchCategoryCount",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CATEGORIES_COUNT, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch category count");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Async thunks for fetching data
export const fetchProducts = createAsyncThunk(
  "admin/fetchProducts",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.PRODUCTS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch products");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchCustomers = createAsyncThunk(
  "admin/fetchCustomers",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CUSTOMERS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch customers");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchOrders = createAsyncThunk(
  "admin/fetchOrders",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ORDERS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch orders");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchTags = createAsyncThunk(
  "admin/fetchTags",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.TAGS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch tags");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchCategories = createAsyncThunk(
  "admin/fetchCategories",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CATEGORIES, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch categories");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchBrands = createAsyncThunk(
  "admin/fetchBrands",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.BRANDS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch brands");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchCustomerOrders = createAsyncThunk(
  "admin/fetchCustomerOrders",
  async (customerId, { rejectWithValue }) => {
    try {
      const response = await fetch(
        `${API_ENDPOINTS.CUSTOMERS}/${customerId}/orders`,
        {
          headers,
        }
      );
      if (!response.ok) throw new Error("Failed to fetch customer orders");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const changePassword = createAsyncThunk(
  "admin/changePassword",
  async (data, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CHANGE_PASSWORD, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const fetchFulfilledOrders = createAsyncThunk(
  "admin/fetchFulfilledOrders",
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.FULLFILLED_ORDERS, {
        headers,
      });
      if (!response.ok) throw new Error("Failed to fetch fulfilled orders");
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Async thunks for posting data
export const postCategory = createAsyncThunk(
  "admin/postCategory",
  async (data, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.CATEGORIES, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to add category");
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const postSubcategory = createAsyncThunk(
  "admin/postSubcategory",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await fetch(
        `${API_ENDPOINTS.CATEGORIES}/${id}/subcategories`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to add subcategory");
      }

      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message || "An unexpected error occurred");
    }
  }
);

export const postBrand = createAsyncThunk(
  "admin/postBrand",
  async (data, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.BRANDS, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to add brand");
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const PostProduct = createAsyncThunk(
  "admin/postProduct",
  async (data, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.ADD_PRODUCT, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to add product");
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// deleteProduct
export const deleteProduct = createAsyncThunk(
  "admin/deleteProduct",
  async (productId, { rejectWithValue }) => {
    try {
      const response = await fetch(API_ENDPOINTS.DELETE_PRODUCT(productId), {
        method: "DELETE",
        headers: headers,
      });
      const responseData = await response.json();

      if (!response.ok) {
        throw new Error(responseData.message || "Failed to delete product");
      }

      return {
        productId,
        message: responseData.message || "Product deleted successfully",
      };
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const adminSlice = createSlice({
  name: "adminData",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    // Products
    builder
      .addCase(fetchProducts.pending, (state) => {
        state.products.status = "loading";
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.products.status = "succeeded";
        state.products.data = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.products.status = "failed";
        state.products.error = action.payload;
      })

      // Customers
      .addCase(fetchCustomers.pending, (state) => {
        state.customers.status = "loading";
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.customers.status = "succeeded";
        state.customers.data = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.customers.status = "failed";
        state.customers.error = action.payload;
      })

      // Orders
      .addCase(fetchOrders.pending, (state) => {
        state.orders.status = "loading";
      })
      .addCase(fetchOrders.fulfilled, (state, action) => {
        state.orders.status = "succeeded";
        state.orders.data = action.payload;
      })
      .addCase(fetchOrders.rejected, (state, action) => {
        state.orders.status = "failed";
        state.orders.error = action.payload;
      })

      // Tags
      .addCase(fetchTags.pending, (state) => {
        state.tags.status = "loading";
      })
      .addCase(fetchTags.fulfilled, (state, action) => {
        state.tags.status = "succeeded";
        state.tags.data = action.payload;
      })
      .addCase(fetchTags.rejected, (state, action) => {
        state.tags.status = "failed";
        state.tags.error = action.payload;
      })

      // Categories
      .addCase(fetchCategories.pending, (state) => {
        state.categories.status = "loading";
      })
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.categories.status = "succeeded";
        state.categories.data = action.payload;
      })
      .addCase(fetchCategories.rejected, (state, action) => {
        state.categories.status = "failed";
        state.categories.error = action.payload;
      })

      // Brands
      .addCase(fetchBrands.pending, (state) => {
        state.brands.status = "loading";
      })
      .addCase(fetchBrands.fulfilled, (state, action) => {
        state.brands.status = "succeeded";
        state.brands.data = action.payload;
      })
      .addCase(fetchBrands.rejected, (state, action) => {
        state.brands.status = "failed";
        state.brands.error = action.payload;
      })

      // Customer Orders
      .addCase(fetchCustomerOrders.pending, (state) => {
        state.customerOrders.status = "loading";
      })
      .addCase(fetchCustomerOrders.fulfilled, (state, action) => {
        state.customerOrders.status = "succeeded";
        state.customerOrders.data = action.payload;
      })
      .addCase(fetchCustomerOrders.rejected, (state, action) => {
        state.customerOrders.status = "failed";
        state.customerOrders.error = action.payload;
      })

      // Post Category
      .addCase(postCategory.pending, (state) => {
        state.categories.status = "loading";
      })
      .addCase(postCategory.fulfilled, (state, action) => {
        state.categories.status = "succeeded";
        state.categories.data.push(action.payload);
      })
      .addCase(postCategory.rejected, (state, action) => {
        state.categories.status = "failed";
        state.categories.error = action.payload;
      })

      // Post Brand
      .addCase(postBrand.pending, (state) => {
        state.brands.status = "loading";
      })
      .addCase(postBrand.fulfilled, (state, action) => {
        state.brands.status = "succeeded";
        state.brands.data.push(action.payload);
      })
      .addCase(postBrand.rejected, (state, action) => {
        state.brands.status = "failed";
        state.brands.error = action.payload;
      });

    // Post Subcategory
    builder
      .addCase(postSubcategory.pending, (state) => {
        state.subcategories.status = "loading";
      })
      .addCase(postSubcategory.fulfilled, (state, action) => {
        state.subcategories.status = "succeeded";
        state.subcategories.data.push(action.payload);
      })
      .addCase(postSubcategory.rejected, (state, action) => {
        state.subcategories.status = "failed";
        state.subcategories.error = action.payload;
      });

    // Delete Product
    builder
      .addCase(deleteProduct.pending, (state) => {
        state.products.status = "loading";
      })
      .addCase(deleteProduct.fulfilled, (state, action) => {
        state.products.status = "succeeded";
        // Remove the deleted product from the products array
        state.products.data = state.products.data.filter(
          (product) => product.id !== action.payload.productId
        );
      })
      .addCase(deleteProduct.rejected, (state, action) => {
        state.products.status = "failed";
        state.products.error = action.payload;
      });

    // Count Fetches
    builder
      .addCase(fetchCustomerCount.fulfilled, (state, action) => {
        state.customersCount.data = action.payload;
        state.customersCount.status = "succeeded";
      })
      .addCase(fetchStockCount.fulfilled, (state, action) => {
        state.productsCount.data = action.payload;
        state.productsCount.status = "succeeded";
      })
      .addCase(fetchRevenue.fulfilled, (state, action) => {
        state.revenue.data = action.payload;
        state.revenue.status = "succeeded";
      })
      .addCase(fetchCategoryCount.fulfilled, (state, action) => {
        state.categoriesCount.data = action.payload;
        state.categoriesCount.status = "succeeded";
      });

    // Fulfilled Orders
    builder
      .addCase(fetchFulfilledOrders.pending, (state) => {
        state.orders.status = "loading";
      })
      .addCase(fetchFulfilledOrders.fulfilled, (state, action) => {
        state.orders.status = "succeeded";
        state.orders.data = action.payload;
      })
      .addCase(fetchFulfilledOrders.rejected, (state, action) => {
        state.orders.status = "failed";
        state.orders.error = action.payload;
      });

    // Post Product
    builder
      .addCase(PostProduct.pending, (state) => {
        state.products.status = "loading";
      })
      .addCase(PostProduct.fulfilled, (state, action) => {
        state.products.status = "succeeded";
        state.products.data.push(action.payload);
      })
      .addCase(PostProduct.rejected, (state, action) => {
        state.products.status = "failed";
        state.products.error = action.payload;
      });

    builder
      .addCase(changePassword.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(changePassword.fulfilled, (state) => {
        state.loading = false;
        state.passwordChanged = true;
      })
      .addCase(changePassword.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || "An error occurred";
      });

    builder
      .addCase(updateOrderStatus.pending, (state) => {
        state.orders.status = "loading";
      })
      .addCase(updateOrderStatus.fulfilled, (state, action) => {
        const { orderId, isFulfilled } = action.payload;
        const order = state.orders.data.find(
          (order) => order.order_id === orderId
        );
        if (order) {
          order.is_fulfilled = isFulfilled;
        }
        state.orders.status = "succeeded";
      })
      .addCase(updateOrderStatus.rejected, (state, action) => {
        state.orders.status = "failed";
        state.orders.error = action.payload;
      });
  },
});

export default adminSlice.reducer;

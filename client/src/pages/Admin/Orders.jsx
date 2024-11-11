import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchOrders, updateOrderStatus } from "../../redux/adminSlice"; // Assuming updateOrderStatus is an action
import { InventoryTable, Loader } from "../../components";

const Orders = () => {
  const dispatch = useDispatch();
  const { orders, loading, error } = useSelector((state) => ({
    orders: state.adminData.orders.data || [],
    loading: state.adminData.orders.status === "loading",
    error: state.adminData.orders.error,
  }));

  const [localOrders, setLocalOrders] = useState(orders);

  useEffect(() => {
    dispatch(fetchOrders());
  }, [dispatch]);

  useEffect(() => {
    setLocalOrders(orders);
  }, [orders]);

  // Handle the status change
  const handleStatusChange = async (orderId, status) => {
    try {
      await dispatch(updateOrderStatus({ orderId, isFulfilled: status }));

      // Update the local state to reflect the change
      setLocalOrders((prevOrders) =>
        prevOrders.map((order) =>
          order.order_id === orderId
            ? { ...order, is_fulfilled: status }
            : order
        )
      );
    } catch (error) {
      console.error("Error updating order status:", error);
    }
  };

  const orderColumns = [
    {
      name: "ID",
      selector: (row) => row.order_id,
      sortable: true,
      maxWidth: "5px",
    },
    {
      name: "Customer Name",
      selector: (row) => `${row.customer.fname} ${row.customer.lname}`,
      sortable: true,
    },
    {
      name: "Email",
      selector: (row) => row.customer.email,
      sortable: true,
    },
    {
      name: "Address",
      selector: (row) =>
        `${row.address.street}, ${row.address.town}, ${row.address.postal_code}, ${row.address.country}`,
      sortable: true,
    },
    {
      name: "Total Items",
      selector: (row) =>
        row.items.reduce((total, item) => total + item.quantity, 0),
      sortable: true,
      maxWidth: "10px",
    },
    {
      name: "Notes",
      selector: (row) => row.notes,
      sortable: false,
    },
    {
      name: "Total",
      selector: (row) => `Ksh. ${row.total_price}`,
      sortable: true,
    },
    {
      name: "Status",
      selector: (row) => row.is_fulfilled,
      cell: (row) => (
        <div className="flex items-center space-x-2">
          {/* Dropdown */}
          <select
            value={row.is_fulfilled ? "Fulfilled" : "Unfulfilled"}
            onChange={(e) =>
              handleStatusChange(row.order_id, e.target.value === "Fulfilled")
            }
            className="px-2 py-1 border rounded-md"
          >
            <option value="Unfulfilled">Unfulfilled</option>
            <option value="Fulfilled">Fulfilled</option>
          </select>

          {/* Status Badge */}
          <span
            className={`px-2 py-1 rounded-[15px] ${
              row.is_fulfilled ? "bg-green-200" : "bg-red-200"
            }`}
          >
            {row.is_fulfilled ? "Fulfilled" : "Unfulfilled"}
          </span>
        </div>
      ),
      sortable: true,
    },
  ];

  return (
    <div className="p-6">
      {loading ? (
        <Loader />
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : orders.length > 0 ? (
        <InventoryTable
          columns={orderColumns}
          title="Order List"
          data={localOrders}
          customStyles={{
            rows: {
              style: {
                minHeight: "72px",
              },
            },
            headCells: {
              style: {
                paddingLeft: "8px !important",
                paddingRight: "8px",
              },
            },
            cells: {
              style: {
                paddingLeft: "8px",
                paddingRight: "8px",
              },
            },
          }}
        />
      ) : (
        <p className="text-gray-500">No orders found.</p>
      )}
    </div>
  );
};

export default Orders;

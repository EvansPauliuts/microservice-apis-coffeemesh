import uuid

from datetime import datetime, timezone

from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from app import app
from api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

orders = []


@app.get('/orders', response_model=GetOrdersSchema)
def get_orders(
    cancelled: bool | None = None,
    limit: int | None = None,
):
    if cancelled is None and limit is None:
        return {'kitchen': orders}

    query_set = list(orders)

    if cancelled is not None:
        if cancelled:
            query_set = [
                order
                for order in query_set
                if order['status'] == 'cancelled'
            ]
        else:
            query_set = [
                order
                for order in query_set
                if order['status'] != 'cancelled'
            ]

    if limit is not None and len(query_set) > limit:
        return {'kitchen': query_set[:limit]}

    return {'kitchen': query_set}


@app.post(
    '/orders',
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.dict()
    order['id'] = uuid.uuid4()
    order['created'] = datetime.now(timezone.utc)
    order['status'] = 'created'
    ORDERS.append(order)
    return order


@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Order with ID {order_id} not found',
    )


@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: uuid.UUID, order_details: CreateOrderSchema):
    for order in ORDERS:
        if order['id'] == order_id:
            order.update(order_details.dict())
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Order with ID {order_id} not found',
    )


@app.delete(
    '/orders/{order_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: uuid.UUID):
    for i, order in enumerate(ORDERS):
        if order['id'] == order_id:
            ORDERS.pop(i)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'cancelled'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Order with ID {order_id} not found'
    )


@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: uuid.UUID):
    for order in ORDERS:
        if order['id'] == order_id:
            order['status'] = 'progress'
            return order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Order with ID {order_id} not found'
    )

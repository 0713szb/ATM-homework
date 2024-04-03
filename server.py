import socket
import pymysql.cursors

# 定义数据库 不用管
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '770078Ab',
    'database': 'atm',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}


# 我只写了这一个函数来对Client端进行响应
def handle_client(client_socket):
    # try...finally是异常处理，不用管
    try:
        # 第一步：接收客户端发送的id
        user_id = client_socket.recv(1024).decode()

        # 连接数据库
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # 检查ID是否存在
            sql = "SELECT id, balance FROM accounts WHERE id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()

            # 顺序执行，if嵌套
            if result:
                # 如果ID存在，发送响应让客户端发送密码
                client_socket.sendall(b"500 sp AUTH REQUIRED!")

                # 第二步：接收密码
                user_password = client_socket.recv(1024).decode()

                # 验证密码
                sql = "SELECT balance FROM accounts WHERE id = %s AND password = %s"
                cursor.execute(sql, (user_id, user_password))
                result = cursor.fetchone()

                # 如果密码正确就进行取款
                if result:
                    client_socket.sendall(b"525 OK!")

                    # 读取存款额
                    user_withdraw = int(client_socket.recv(1024).decode())

                    # 读取该ID中的余额
                    balance = result['balance']

                    # 能够取款
                    if balance >= user_withdraw:

                        # 更新数据库
                        new_balance = balance - user_withdraw
                        sql = "UPDATE accounts SET balance=%s WHERE id=%s"
                        cursor.execute(sql, (new_balance, user_id))
                        connection.commit()

                        # 发送响应，取款成功
                        client_socket.sendall(f"SUCCESS:you have {new_balance} left in your balance!".encode())

                        # 接收结束语
                        user_over = client_socket.recv(1024).decode()

                        if user_over == "bye":
                            # 发送响应，结束服务
                            client_socket.sendall(b"BYE!")

                    # 余额不足
                    else:
                        client_socket.sendall(b"401 sp ERROR!")

                else:
                    # 密码不正确
                    client_socket.sendall(b"Invalid password.")

            else:
                # ID不正确
                client_socket.sendall(b"ID not found.")
                client_socket.close()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 2525))
    server_socket.listen(5)
    print("Server is listening on port 2525...")

    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)


if __name__ == "__main__":
    main()

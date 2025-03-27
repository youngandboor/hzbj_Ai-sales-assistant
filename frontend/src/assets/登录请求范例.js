// 1. 首先获取CSRF token
const getCsrfToken = async () => {
  const response = await axios.get('http://localhost:8000/api/auth/csrf/', {
    withCredentials: true,
    headers: {
      'Accept': 'application/json'
    }
  });
  return response.data.csrfToken;
};

// 2. 登录请求
const login = async (username, password) => {
  try {
    // 获取CSRF token
    const csrfToken = await getCsrfToken();
    
    // 发送登录请求
    const response = await axios.post('http://localhost:8000/api/auth/login/', 
      {
        username: username,
        password: password
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      }
    );
    
    return response.data;
  } catch (error) {
    console.error('登录失败:', error);
    throw error;
  }
};
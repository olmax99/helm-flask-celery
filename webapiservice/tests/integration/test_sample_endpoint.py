"""
Integration Tests:
  1. In SampleCompute test send_task() success and failure
  2. In JobCheck test AsyncResult() success and failure
  3. In JobCheck test redis interaction

"""

# Your development environment is exactly the same as your test environment

# -----------------------------------------------
#   Does the message broker receive the task?
# -----------------------------------------------
# 1. Start the production ready package of the app under test.
#   - How to start Minikube as a fixture?
# 2. Start an instance of all the dependency systems required.
# 3. Run tests that interact only via the public service endpoints with the app.
# 4. Nothing is persisted between executions, so we don’t have to worry about restoring the initial state.
# 5. Resources are allocated only during test execution.

# 1. If send_task() is successful, can the task be found in redis


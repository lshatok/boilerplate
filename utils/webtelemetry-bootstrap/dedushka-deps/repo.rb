dep 'pull repo.task' do
  requires 'common:clean.repo'
  run do
    shell('git fetch')
  end
end
